import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin List (Secure Verification)
ADMIN_IDS = set(map(int, filter(None, os.getenv("ADMIN_IDS", "6836865426").split(","))))

# Other Settings
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/your_channel")
BOT_USERNAME = os.getenv("BOT_USERNAME", "ProMediaDownloaderBot")

# Render Port Configuration
PORT = int(os.getenv("PORT", "10000"))

# Bot Limits
MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "3"))
MAX_FILE_SIZE = 50 * 1024 * 1024  # Telegram API limit 50MB
TEMP_DIR = "downloads/"

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)
