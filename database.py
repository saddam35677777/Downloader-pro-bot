import aiosqlite
import datetime
from config import ADMIN_IDS

DB_NAME = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                lang TEXT DEFAULT 'en',
                is_premium INTEGER DEFAULT 0,
                premium_plan TEXT DEFAULT 'FREE',
                is_banned INTEGER DEFAULT 0,
                join_date TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                media_title TEXT,
                media_type TEXT,
                quality TEXT,
                timestamp TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                action TEXT,
                target_user INTEGER,
                timestamp TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        await db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', '0')")
        await db.commit()

async def get_setting(key):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT value FROM settings WHERE key=?", (key,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def set_setting(key, value):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        await db.commit()

async def add_user(user_id, name, username):
    async with aiosqlite.connect(DB_NAME) as db:
        join_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, name, username, join_date)
            VALUES (?, ?, ?, ?)
        """, (user_id, name, username, join_date))
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id=?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def update_user_lang(user_id, lang):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
        await db.commit()

async def log_download(user_id, title, media_type, quality):
    async with aiosqlite.connect(DB_NAME) as db:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("""
            INSERT INTO downloads (user_id, media_title, media_type, quality, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, media_type, quality, timestamp))
        await db.commit()

async def get_stats():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as c: total_users = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM downloads") as c: total_dl = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM users WHERE is_premium=1") as c: total_prem = (await c.fetchone())[0]
        return total_users, total_dl, total_prem
