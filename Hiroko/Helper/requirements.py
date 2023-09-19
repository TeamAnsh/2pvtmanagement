import asyncio
from os import path
import os
from Hiroko.Helper.errors import FFmpegReturnCodeError, DurationLimitError
from yt_dlp import YoutubeDL
from typing import List, Dict, Union
from asyncio import Queue, QueueEmpty as Empty
from pyrogram.types import *



DURATION_LIMIT = 300

active = []


async def get_active_chats() -> list:
    return active

# ===================================================================================== #

admins: Dict[int, List[int]] = {}


def set_admins(chat_id: int, admins_: List[int]):
    admins[chat_id] = admins_


def get_admins(chat_id: int) -> Union[List[int], bool]:
    return admins.get(chat_id, False)

# ===================================================================================== #

def get_url(message_1: Message) -> Union[str, None]:
    messages = [message_1]

    if message_1.reply_to_message:
        messages.append(message_1.reply_to_message)

    text = ""
    offset = None
    length = None

    for message in messages:
        if offset:
            break

        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break

    if offset is None:
        return None

    return text[offset:offset + length]

def get_file_name(audio: Union[Audio, Voice]):
    ext = audio.file_name.split(".")[-1] if not isinstance(audio, Voice) else "ogg"
    return f'{audio.file_unique_id}.{ext}'

# ===================================================================================== #



def downloader(url: str) -> str:
    download_directory = os.path.join("Hiroko", "Helper", "downloader", "downloads")
    
    ydl_opts = {
        "format": "bestaudio/best",
        "geo-bypass": True,
        "nocheckcertificate": True,
        "outtmpl": os.path.join(download_directory, "%(id)s.%(ext)s"),
    }

    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 Videos longer than {DURATION_LIMIT} minute(s) are not allowed, the provided is {duration} minute(s)"
        )

    try:
        ydl.download([url])
    except Exception as e:
        raise DurationLimitError(
            f"🛑 Videos longer than {DURATION_LIMIT} minute(s) are not allowed, the provided is {duration} minute(s)"
        )

    return os.path.join(download_directory, f"{info['id']}.{info['ext']}")

async def converter(file_path: str) -> str:
    raw_directory = os.path.join("Hiroko", "Helper", "downloader", "raw_files")
    
    out = os.path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = os.path.basename(out)
    out = os.path.join(raw_directory, out)

    # Ensure the 'raw_files' directory exists
    os.makedirs(raw_directory, exist_ok=True)

    if os.path.isfile(out):
        return out

    try:
        proc = await asyncio.create_subprocess_shell(
            cmd=(
                "ffmpeg " 
                "-y -i " 
                f"{file_path} "
                "-f s16le "
                "-ac 1 "
                "-ar 48000 "
                "-acodec pcm_s16le " 
                f"{out}"
            ),
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise FFmpegReturnCodeError(f"FFmpeg did not return 0: {stderr.decode()}")

        return out
    except Exception as e:
        raise FFmpegReturnCodeError(f"FFmpeg did not return 0: {str(e)}")




# ===================================================================================== #


queues: Dict[int, Queue] = {}

async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()

def get(chat_id: int) -> Dict[str, str]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None

def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True

def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass

def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].queue = []
    raise Empty


# ===================================================================================== #


