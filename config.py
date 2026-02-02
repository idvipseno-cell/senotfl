import os

# إعدادات البوت الرئيسية
MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN", "YOUR_MAIN_BOT_TOKEN_HERE")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "123456789").split(",")]

# قناة الاشتراك الإجباري
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "@YourChannelUsername")

# --- قائمة التفاعلات ---

# التفاعلات العادية
STANDARD_REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡️", "🍌", "🏆", "💎", "🍓", "🍾", "💋", "🖕", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "💪", "🙌", "✍️", "🤝", "👍", "👎"]

# التفاعلات المميزة (التي تعتبر "Special" في مجتمع التلغرام)
PREMIUM_REACTIONS = [
    "👨‍💻", "🐳", "🤝", "😇", "🫡", "🤔", "👨‍🏫", "🔍", "🎯", "🏆", "💔", "🌚", "⚡️", "🍌", 
    "💊", "🗿", "🆒", "🍓", "🍑", "🍾", "🍿", "🍕", "🍔", "🍟", "🍦", "🍩", "🍪", "🎂",
    "🍰", "🧁", "🥧", "🍫", "🍬", "🍭", "🍮", "🍯", "🍼", "☕️", "🍵", "🥤", "🍶", "🍺"
]

# دمج القوائم للحصول على تنوع كامل
ALL_REACTIONS = list(set(STANDARD_REACTIONS + PREMIUM_REACTIONS))

# إعدادات قاعدة البيانات
DB_PATH = os.getenv("DB_PATH", "/home/ubuntu/reaction_bot_project/database/bot_data.db")
