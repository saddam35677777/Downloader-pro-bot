# PRO MEDIA DOWNLOADER 🎬

A professional, modular, and production-ready Telegram Bot for downloading and processing media. 

## Features
- yt-dlp integrated for Video and Audio downloads.
- FFmpeg support for Video Cutting, GIF making, and Audio extraction.
- Professional Inline Keyboard UI.
- Secure Admin Panel.
- Download queuing system to prevent bot crashes.
- SQLite Database for user management.
- Multi-language (Bangla & English).

## Setup & Run Locally

1. **Clone the repository.**
2. **Install requirements:**
   `pip install -r requirements.txt`
3. **Install FFmpeg** on your local machine and ensure it's in your system PATH.
4. **Create a `.env` file** in the root directory:
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_IDS=6836865426
   PORT=10000
