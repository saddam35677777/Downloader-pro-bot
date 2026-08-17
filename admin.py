from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_IDS
import database
import os
import psutil

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
         InlineKeyboardButton("👥 Users", callback_data="admin_users")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
         InlineKeyboardButton("🧹 Storage Cleanup", callback_data="admin_cleanup")],
        [InlineKeyboardButton("🖥 Server Status", callback_data="admin_server"),
         InlineKeyboardButton("🔧 Maintenance Mode", callback_data="admin_maintenance")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "👑 <b>ADMIN CONTROL CENTER</b>\n\nWelcome Super Admin. Choose an option:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def admin_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    if user_id not in ADMIN_IDS:
        await query.answer("⛔ Admin Only!", show_alert=True)
        return

    if data == "admin_stats":
        total_u, total_d, total_p = await database.get_stats()
        text = f"📊 <b>BOT STATISTICS</b>\n\n👥 Total Users: {total_u}\n📥 Total Downloads: {total_d}\n⭐ Premium Users: {total_p}"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        
    elif data == "admin_server":
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        text = f"🖥 <b>SERVER STATUS</b>\n\n⚙️ CPU Usage: {cpu}%\n🧠 RAM Usage: {ram}%\n💾 Disk Usage: {disk}%"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        
    elif data == "admin_cleanup":
        from config import TEMP_DIR
        import shutil
        count = 0
        for f in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    count += 1
            except: pass
        await query.answer(f"🧹 Cleaned {count} temporary files.", show_alert=True)
        
    elif data == "admin_panel":
        await admin_panel(update, context)
