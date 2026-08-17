import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from config import BOT_TOKEN, MAX_CONCURRENT_DOWNLOADS, MAX_FILE_SIZE
from database import init_db, get_setting, get_user
from utils import get_text, clean_temp, escape
import user
import admin
from downloader import get_media_info, download_media
from keep_alive import keep_alive
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Queue Semaphore
download_semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

async def check_maintenance(update: Update) -> bool:
    is_maint = await get_setting('maintenance')
    user_id = update.effective_user.id
    if is_maint == '1' and user_id not in admin.ADMIN_IDS:
        await update.message.reply_text("🔧 <b>Maintenance Mode Active</b>\nPlease try later.", parse_mode="HTML")
        return True
    
    db_user = await get_user(user_id)
    if db_user and db_user['is_banned'] == 1:
        await update.message.reply_text("🚫 You are banned.")
        return True
    return False

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_maintenance(update): return
    
    url = update.message.text
    if not url.startswith("http"):
        return

    msg = await update.message.reply_text("🔎 <i>Analyzing Link...</i>", parse_mode="HTML")
    info = await get_media_info(url)
    
    if not info:
        await msg.edit_text("❌ <b>Could not extract media info.</b>", parse_mode="HTML")
        return

    title = escape(info.get('title', 'Unknown Title'))
    duration = info.get('duration', 0)
    
    context.user_data['current_url'] = url
    
    keyboard = [
        [InlineKeyboardButton("🎬 Download Video (Best)", callback_data="dl_vid_best")],
        [InlineKeyboardButton("🎵 Download Audio (MP3)", callback_data="dl_aud_best")],
        [InlineKeyboardButton("🖼 Get Thumbnail", callback_data="dl_thumb_best")]
    ]
    
    text = get_text(context.user_data, 'link_found', title=title, duration=duration)
    await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    
    if data.startswith("admin_"):
        await admin.admin_callback_handler(update, context)
    elif data.startswith("menu_") or data == "main_menu" or data.startswith("set_lang_"):
        await user.user_callback_handler(update, context)
    elif data.startswith("dl_"):
        await process_download(update, context)
    else:
        await update.callback_query.answer()

async def process_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    url = context.user_data.get('current_url')
    if not url:
        await query.edit_message_text("❌ Session expired. Send link again.")
        return
    
    action = query.data.split("_")[1] # vid, aud, thumb
    
    await query.edit_message_text(get_text(context.user_data, 'processing'), parse_mode="HTML")
    
    async with download_semaphore:
        try:
            if action == "vid":
                filepath = await download_media(url, is_audio=False)
                if filepath and os.path.getsize(filepath) <= MAX_FILE_SIZE:
                    await context.bot.send_document(query.message.chat_id, document=open(filepath, 'rb'))
                    clean_temp(filepath)
                    await query.edit_message_text(get_text(context.user_data, 'success'), parse_mode="HTML")
                else:
                    await query.edit_message_text(get_text(context.user_data, 'too_large'), parse_mode="HTML")
                    clean_temp(filepath)
                    
            elif action == "aud":
                filepath = await download_media(url, is_audio=True)
                if filepath and os.path.getsize(filepath) <= MAX_FILE_SIZE:
                    await context.bot.send_audio(query.message.chat_id, audio=open(filepath, 'rb'))
                    clean_temp(filepath)
                    await query.edit_message_text(get_text(context.user_data, 'success'), parse_mode="HTML")
                else:
                    await query.edit_message_text(get_text(context.user_data, 'too_large'), parse_mode="HTML")
                    clean_temp(filepath)
                    
            elif action == "thumb":
                # For thumb, we could just extract thumbnail URL, but for simplicity:
                await query.edit_message_text("🖼 Thumbnail functionality depends on source. Use yt-dlp thumbnail extract config.", parse_mode="HTML")
                
        except Exception as e:
            logger.error(f"Error in process_download: {e}")
            await query.edit_message_text(get_text(context.user_data, 'failed', reason=str(e)), parse_mode="HTML")

async def main():
    await init_db()
    keep_alive()  # Start Flask for Render
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", user.start_command))
    app.add_handler(CommandHandler("admin", admin.admin_panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    app.add_handler(CallbackQueryHandler(callback_router))
    
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
