import asyncio
import Hiroko.Helper.admins
from yt_dlp import YoutubeDL
from typing import List, Dict, Union
from asyncio import Queue, QueueEmpty as Empty
from pyrogram.types import *
from os import path

DURATION_LIMIT = "300"





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

    if offset in (None,):
        return None

    return text[offset:offset + length]


def get_file_name(audio: Union[Audio, Voice]):
    return f'{audio.file_unique_id}.{audio.file_name.split(".")[-1] if not isinstance(audio, Voice) else "ogg"}'


# ===================================================================================== #


class DurationLimitError(Exception):
    pass

class FFmpegReturnCodeError(Exception):
    pass


# ===================================================================================== #

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 ᴠɪᴅᴇᴏs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ(s) ᴀʀᴇ'ᴛ ᴀʟʟᴏᴡᴇᴅ, ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ɪs {duration} ᴍɪɴᴜᴛᴇ(s)",
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 ᴠɪᴅᴇᴏs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ(s) ᴀʀᴇ'ᴛ ᴀʟʟᴏᴡᴇᴅ, ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ɪs {duration} ᴍɪɴᴜᴛᴇ(s)",
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")


# ===================================================================================== #


async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 1 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    if proc.returncode != 0:
        raise FFmpegReturnCodeError("FFmpeg did not return 0")

    return out


# ===================================================================================== #


async def get_administrators(chat: Chat) -> List[User]:
    get = Hiroko.Helper.admins.get(chat.id)

    if get:
        return get
    else:
        administrators = await chat.get_members(filter="administrators")
        to_set = []

        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                to_set.append(administrator.user.id)

        Hiroko.Helper.admins.set(chat.id, to_set)
        return to_set


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

