import os
import asyncio
import uuid
from config import TEMP_DIR
from utils import clean_temp

async def run_cmd(*args):
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode == 0

async def extract_audio(video_path: str, format_ext: str = "mp3") -> str:
    out_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.{format_ext}")
    success = await run_cmd("ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", out_path, "-y")
    if success and os.path.exists(out_path):
        return out_path
    clean_temp(out_path)
    return None

async def create_gif(video_path: str, duration: int = 5) -> str:
    out_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.gif")
    success = await run_cmd(
        "ffmpeg", "-i", video_path, "-t", str(duration),
        "-vf", "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0", out_path, "-y"
    )
    if success and os.path.exists(out_path):
        return out_path
    clean_temp(out_path)
    return None

async def cut_video(video_path: str, start: str, end: str) -> str:
    out_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_cut.mp4")
    success = await run_cmd("ffmpeg", "-i", video_path, "-ss", start, "-to", end, "-c", "copy", out_path, "-y")
    if success and os.path.exists(out_path):
        return out_path
    clean_temp(out_path)
    return None
