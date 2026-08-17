from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database

async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐ Buy PRO Plan", callback_data="buy_pro")],
        [InlineKeyboardButton("🌟 Buy ULTRA Plan", callback_data="buy_ultra")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu")]
    ]
    text = (
        "⭐ <b>PREMIUM SYSTEM</b>\n\n"
        "Unlock maximum speeds, larger file sizes, and advanced processing tools!\n\n"
        "<i>Note: Automatic payments are in development. Contact Admin to upgrade manually.</i>"
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
