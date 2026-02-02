import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='/home/ubuntu/reaction_bot_project/database/bot_data.db'):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    is_admin INTEGER DEFAULT 0,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # جدول القنوات المفعلة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id INTEGER PRIMARY KEY,
                    owner_id INTEGER,
                    channel_username TEXT,
                    is_active INTEGER DEFAULT 1,
                    FOREIGN KEY (owner_id) REFERENCES users(user_id)
                )
            ''')
            # جدول البوتات الثانوية (التوكنات)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS secondary_bots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    bot_username TEXT,
                    is_working INTEGER DEFAULT 1
                )
            ''')
            # جدول إعدادات النظام (مثل القناة الإجبارية)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            conn.commit()

    def add_user(self, user_id, username):
        with self._get_connection() as conn:
            conn.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))

    def add_channel(self, channel_id, owner_id, channel_username):
        with self._get_connection() as conn:
            conn.execute('INSERT OR REPLACE INTO channels (channel_id, owner_id, channel_username) VALUES (?, ?, ?)', 
                         (channel_id, owner_id, channel_username))

    def remove_channel(self, channel_id):
        with self._get_connection() as conn:
            conn.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))

    def get_active_channels(self):
        with self._get_connection() as conn:
            return conn.execute('SELECT channel_id FROM channels WHERE is_active = 1').fetchall()

    def add_secondary_bot(self, token, bot_username):
        with self._get_connection() as conn:
            conn.execute('INSERT OR IGNORE INTO secondary_bots (token, bot_username) VALUES (?, ?)', (token, bot_username))

    def get_secondary_bots(self):
        with self._get_connection() as conn:
            return conn.execute('SELECT token FROM secondary_bots WHERE is_working = 1').fetchall()

    def set_setting(self, key, value):
        with self._get_connection() as conn:
            conn.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))

    def get_setting(self, key):
        with self._get_connection() as conn:
            result = conn.execute('SELECT value FROM settings WHERE key = ?', (key,)).fetchone()
            return result[0] if result else None
