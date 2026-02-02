import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
import sys
sys.path.append('/home/ubuntu/reaction_bot_project')
from config import DEFAULT_REACTIONS
from database.db_manager import DatabaseManager
import random

logging.basicConfig(level=logging.INFO)
db = DatabaseManager()

async def run_bot(token):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.channel_post()
    async def handle_channel_post(message: Message):
        channel_id = message.chat.id
        # التحقق من أن القناة مفعلة في قاعدة البيانات
        active_channels = [c[0] for c in db.get_active_channels()]
        if channel_id in active_channels:
            try:
                # اختيار تفاعل عشوائي
                reaction = random.choice(DEFAULT_REACTIONS)
                # استخدام setMessageReaction
                # ملاحظة: aiogram 3.x يدعم هذا عبر react
                await message.react([types.ReactionTypeEmoji(emoji=reaction)])
                logging.info(f"Bot {token[:10]}... reacted to {channel_id}")
            except Exception as e:
                logging.error(f"Error in bot {token[:10]}: {e}")

    try:
        logging.info(f"Starting bot: {token[:10]}...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Failed to start bot {token[:10]}: {e}")

async def main():
    # جلب جميع توكنات البوتات الثانوية من قاعدة البيانات
    tokens = [t[0] for t in db.get_secondary_bots()]
    
    if not tokens:
        logging.warning("No secondary bots found in database!")
        # إضافة توكن تجريبي إذا كانت القاعدة فارغة (للمستخدم لإضافتها لاحقاً)
        return

    tasks = [run_bot(token) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
