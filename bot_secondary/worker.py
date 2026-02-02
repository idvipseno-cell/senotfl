import asyncio
import logging
from telethon import TelegramClient, events, types
import sys
sys.path.append('/home/ubuntu/reaction_bot_project')
from config import DEFAULT_REACTIONS
from database.db_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
db = DatabaseManager()

# ملاحظة: سنستخدم مكتبة Telethon لأنها تدعم تشغيل عدة بوتات بسهولة في نفس الحلقة
# ولكن للتبسيط هنا سننشئ نموذجاً يشرح كيفية عمل البوتات الثانوية

async def start_secondary_bot(token):
    # API_ID و API_HASH مطلوبان لـ Telethon
    # يمكن للمستخدم الحصول عليهما من my.telegram.org
    api_id = 1234567  # سيتم استبدالها بقيم حقيقية
    api_hash = 'your_api_hash'
    
    bot = TelegramClient(f'sessions/bot_{token[:10]}', api_id, api_hash)
    
    @bot.on(events.NewMessage(func=lambda e: e.is_channel))
    async def handler(event):
        channel_id = event.chat_id
        # التحقق إذا كانت القناة مسجلة في قاعدة البيانات
        active_channels = [c[0] for c in db.get_active_channels()]
        if channel_id in active_channels:
            try:
                # اختيار تفاعل عشوائي من القائمة
                import random
                reaction = random.choice(DEFAULT_REACTIONS)
                # استخدام ميزة التفاعل في تلغرام
                await bot(types.functions.messages.SendReactionRequest(
                    peer=event.input_chat,
                    msg_id=event.id,
                    reaction=[types.ReactionEmoji(emoticon=reaction)]
                ))
                logging.info(f"Bot reacted to message {event.id} in channel {channel_id}")
            except Exception as e:
                logging.error(f"Error reacting: {e}")

    await bot.start(bot_token=token)
    await bot.run_until_disconnected()

# هذا الملف هو مجرد نموذج لكيفية عمل "العمال" (Workers)
# في النسخة النهائية، سيتم تشغيل البوتات الثانوية بشكل متوازٍ
