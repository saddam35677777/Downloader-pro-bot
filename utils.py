import os
import shutil
import html
from config import ADMIN_IDS, TEMP_DIR

LANGUAGES = {
    'en': {
        'welcome': "🎬 <b>PRO MEDIA DOWNLOADER</b>\n\nWelcome to the ultimate media downloader bot. Please select an option below:",
        'maintenance': "🔧 <b>Maintenance Mode</b>\nThe bot is currently under maintenance. Please try again later.",
        'banned': "🚫 You are banned from using this bot.",
        'link_found': "🔗 <b>MEDIA FOUND</b>\n\n🎬 Title: {title}\n⏱ Duration: {duration}s\n\nSelect action:",
        'processing': "⚙️ <b>Processing your request in queue...</b>",
        'success': "✅ <b>Task Completed!</b>",
        'failed': "❌ <b>Task Failed.</b>\nReason: {reason}",
        'too_large': "❌ <b>File too large!</b> Telegram restricts files over 50MB.",
        'admin_only': "⛔ Access Denied. Super Admin only."
    },
    'bn': {
        'welcome': "🎬 <b>প্রো মিডিয়া ডাউনলোডার</b>\n\nসেরা মিডিয়া ডাউনলোডার বটে আপনাকে স্বাগতম। নিচের মেনু থেকে অপশন বেছে নিন:",
        'maintenance': "🔧 <b>মেইনটেন্যান্স মোড</b>\nবটটিতে বর্তমানে আপডেট চলছে। কিছুক্ষণ পর আবার চেষ্টা করুন।",
        'banned': "🚫 আপনাকে বট ব্যবহারে নিষিদ্ধ করা হয়েছে।",
        'link_found': "🔗 <b>মিডিয়া পাওয়া গেছে</b>\n\n🎬 নাম: {title}\n⏱ সময়: {duration}s\n\nকী করতে চান?",
        'processing': "⚙️ <b>আপনার রিকোয়েস্টটি কিউ-তে প্রসেস হচ্ছে...</b>",
        'success': "✅ <b>কাজ সম্পন্ন হয়েছে!</b>",
        'failed': "❌ <b>কাজটি ব্যর্থ হয়েছে।</b>\nকারণ: {reason}",
        'too_large': "❌ <b>ফাইল সাইজ অনেক বড়!</b> টেলিগ্রামে ৫০ এমবির বেশি ফাইল পাঠানো যায় না।",
        'admin_only': "⛔ অ্যাক্সেস ডিনাইড। শুধুমাত্র সুপার অ্যাডমিন এটি ব্যবহার করতে পারবেন।"
    }
}

def get_text(user_data, key, **kwargs):
    lang = user_data.get('lang', 'en')
    text = LANGUAGES.get(lang, LANGUAGES['en']).get(key, "TEXT NOT FOUND")
    if kwargs:
        return text.format(**kwargs)
    return text

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def escape(text: str) -> str:
    return html.escape(str(text))

def clean_temp(filepath: str):
    if filepath and os.path.exists(filepath):
        try:
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)
        except Exception as e:
            print(f"Cleanup error: {e}")
