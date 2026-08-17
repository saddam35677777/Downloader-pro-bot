from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database
from utils import get_text
from premium import premium_menu
from config import ADMIN_IDS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await database.add_user(user.id, user.first_name, user.username)
    
    # Store lang in context safely
    db_user = await database.get_user(user.id)
    lang = db_user['lang'] if db_user else 'en'
    context.user_data['lang'] = lang

    await main_menu(update, context)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = context.user_data.get('lang', 'en')
    
    keyboard = [
        [InlineKeyboardButton("🔗 Download Media", callback_data="menu_dl_media"),
         InlineKeyboardButton("🎵 Audio Downloader", callback_data="menu_dl_audio")],
        [InlineKeyboardButton("🎬 Video → Audio", callback_data="menu_vid_audio"),
         InlineKeyboardButton("✂️ Video Cutter", callback_data="menu_vid_cut")],
        [InlineKeyboardButton("🎞 GIF Maker", callback_data="menu_gif"),
         InlineKeyboardButton("🖼 Thumbnail", callback_data="menu_thumb")],
        [InlineKeyboardButton("📜 History", callback_data="menu_history"),
         InlineKeyboardButton("👤 Profile", callback_data="menu_profile")],
        [InlineKeyboardButton("⭐ Premium", callback_data="menu_premium"),
         InlineKeyboardButton("🌐 Language", callback_data="menu_lang")]
    ]
    
    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("👑 ADMIN PANEL", callback_data="admin_panel")])

    text = get_text(context.user_data, 'welcome')
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def user_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "main_menu":
        await main_menu(update, context)
    elif data == "menu_lang":
        kb = [[InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en"),
               InlineKeyboardButton("🇧🇩 বাংলা", callback_data="set_lang_bn")]]
        await query.edit_message_text("🌐 Select Language / ভাষা নির্বাচন করুন:", reply_markup=InlineKeyboardMarkup(kb))
    elif data.startswith("set_lang_"):
        lang = data.split("_")[2]
        await database.update_user_lang(query.from_user.id, lang)
        context.user_data['lang'] = lang
        await query.answer("Language updated! / ভাষা আপডেট হয়েছে!", show_alert=True)
        await main_menu(update, context)
    elif data == "menu_premium":
        await premium_menu(update, context)
    elif data == "menu_profile":
        db_user = await database.get_user(query.from_user.id)
        if db_user:
            plan = db_user['premium_plan']
            joined = db_user['join_date']
            text = f"👤 <b>MY PROFILE</b>\n\n🆔 ID: <code>{db_user['user_id']}</code>\n📛 Name: {db_user['name']}\n⭐ Plan: <b>{plan}</b>\n📅 Joined: {joined}"
            kb = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
