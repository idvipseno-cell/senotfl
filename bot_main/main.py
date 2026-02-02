import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOINED, LEFT

import sys
sys.path.append('/home/ubuntu/reaction_bot_project')
from config import MAIN_BOT_TOKEN, ADMIN_IDS, REQUIRED_CHANNEL
from database.db_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
bot = Bot(token=MAIN_BOT_TOKEN)
dp = Dispatcher()
db = DatabaseManager()

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username)
    
    if not await check_subscription(user_id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="اشترك في القناة", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")],
            [InlineKeyboardButton(text="تم الاشتراك ✅", callback_data="check_sub")]
        ])
        await message.answer(f"⚠️ يجب عليك الاشتراك في قناة البوت أولاً لاستخدام الخدمة:\n{REQUIRED_CHANNEL}", reply_markup=kb)
        return

    welcome_text = (
        "❤️ أهلاً بك في بوت التفاعلات المميزة\n\n"
        "هذا البوت يساعدك على زيادة التفاعل في قناتك تلقائياً.\n"
        "للبدء، قم بإضافة البوت الرئيسي والبوتات المساعدة كمشرفين في قناتك.\n\n"
        "📌 شروط تفعيل البوت:\n"
        "1. أن تكون قناتك عامة.\n"
        "2. رفع البوت الرئيسي مشرفاً.\n"
        "3. عدم مغادرة قناة السورس وإلا سيتعطل البوت.\n\n"
        "استخدم القائمة أدناه للتحكم:"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ إضافة قناة", callback_data="add_channel")],
        [InlineKeyboardButton(text="📊 إحصائياتي", callback_data="my_stats")],
        [InlineKeyboardButton(text="📢 قناة السورس", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")]
    ])
    
    if user_id in ADMIN_IDS:
        kb.inline_keyboard.append([InlineKeyboardButton(text="🛠 لوحة الآدمن", callback_data="admin_panel")])
        
    await message.answer(welcome_text, reply_markup=kb)

@dp.callback_query(F.data == "add_channel")
async def add_channel_prompt(callback: types.CallbackQuery):
    await callback.message.answer("أرسل الآن معرف قناتك (مثلاً: @MyChannel) أو قم بتوجيه رسالة منها هنا.\nتأكد من رفع البوت مشرفاً أولاً!")

@dp.message(F.text.startswith("@") | F.forward_from_chat)
async def process_channel_addition(message: types.Message):
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        await message.answer("عذراً، يجب أن تشترك في القناة الإجبارية أولاً.")
        return

    channel_id = None
    channel_username = None

    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        channel_username = message.forward_from_chat.username
    else:
        channel_username = message.text.strip()
        try:
            chat = await bot.get_chat(channel_username)
            channel_id = chat.id
        except Exception:
            await message.answer("❌ لم أتمكن من العثور على القناة. تأكد من المعرف وأن القناة عامة.")
            return

    # التحقق من صلاحيات البوت في القناة
    try:
        member = await bot.get_chat_member(channel_id, bot.id)
        if member.status != "administrator":
            await message.answer("❌ يجب رفع البوت مشرفاً في القناة أولاً!")
            return
    except Exception:
        await message.answer("❌ حدث خطأ أثناء التحقق من القناة. تأكد من إضافة البوت.")
        return

    db.add_channel(channel_id, user_id, channel_username)
    await message.answer(f"✅ تم تفعيل التفاعل التلقائي لقناتك: {channel_username}\nسيحصل كل منشور جديد على تفاعلات من جميع البوتات الثانوية.")

# تتبع مغادرة القناة الإجبارية
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT))
async def on_user_left(event: ChatMemberUpdated):
    if str(event.chat.id) in REQUIRED_CHANNEL or event.chat.username == REQUIRED_CHANNEL.replace("@", ""):
        user_id = event.from_user.id
        # تعطيل جميع قنوات هذا المستخدم
        with db._get_connection() as conn:
            conn.execute('UPDATE channels SET is_active = 0 WHERE owner_id = ?', (user_id,))
        logging.info(f"User {user_id} left required channel. Deactivated their channels.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
