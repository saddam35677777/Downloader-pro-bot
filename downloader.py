import os
import uuid
import asyncio
import yt_dlp
from config import TEMP_DIR
from utils import clean_temp

def fetch_info_sync(url: str):
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

async def get_media_info(url: str):
    try:
        return await asyncio.to_thread(fetch_info_sync, url)
    except Exception as e:
        print(f"Info Error: {e}")
        return None

def download_sync(url: str, format_id: str, is_audio: bool):
    filename = f"{uuid.uuid4()}"
    out_tmpl = os.path.join(TEMP_DIR, f"{filename}.%(ext)s")
    
    ydl_opts = {
        'format': format_id if not is_audio else 'bestaudio/best',
        'outtmpl': out_tmpl,
        'quiet': True,
    }
    
    if is_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if is_audio:
                return os.path.join(TEMP_DIR, f"{info['id']}.mp3") # Simplified approach
            else:
                return ydl.prepare_filename(info)
    except Exception as e:
        print(f"Download error: {e}")
        return None

async def download_media(url: str, format_id: str = "best", is_audio: bool = False):
    return await asyncio.to_thread(download_sync, url, format_id, is_audio)
