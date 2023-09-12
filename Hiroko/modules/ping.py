import time
import random
from asyncio import sleep as rest
from pyrogram import Client, filters
from pyrogram.types import Message
from Hiroko import boot as tim
from Hiroko import Hiroko
from config import OWNER_ID as owner
from config import SUDO_USERS as sudo
from pyrogram import filters, __version__
from platform import python_version
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)



# ------------------------------------------------------------------------------- #


photo = [
"https://graph.org/file/2fc37c68163780e31599f.jpg",
"https://graph.org/file/3cc07627bdec5f5afab1c.jpg",
"https://graph.org/file/809fe233d8f7c29c6fd69.jpg",
"https://graph.org/file/677619500837cd3190c6d.jpg",
"https://graph.org/file/2a4d6cfdf60a38130aad2.jpg",
"https://graph.org/file/066ed5867fe94c333c0b6.jpg",
"https://graph.org/file/bd06b509e025bc656766d.jpg",
"https://graph.org/file/cd33fd3d193ac98486eff.jpg",
"https://graph.org/file/9ffb36ba7d53b7894eaba.jpg",
"https://graph.org/file/fe6dc66f7968ea69dcec0.jpg",
"https://graph.org/file/917d3b7324a056d66a8cb.jpg",
"https://graph.org/file/4f46ebdf26f703f1d5e93.jpg",
"https://graph.org/file/b3d7c31922a85e94e9627.jpg",
"https://graph.org/file/82560acb529e63c9ddb94.jpg",

]

# ------------------------------------------------------------------------------- #

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


sudo.append(owner)

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["ping"], prefixes=["/", "!"]))
async def ping(Client, m: Message):
    start_time = time.time()
    sender = m.from_user
    up = get_readable_time((time.time() - tim))
    end_time = time.time()
    ping1 = str(round((end_time - start_time) * 1000, 3)) + " ms"
    if m.from_user.id in sudo:
        e = await m.reply_photo(photo=random.choice(photo),caption="ɢᴇᴛᴛɪɴɢ ᴘɪɴɢɪɴɢ sᴛᴀᴛᴜs...")
        await rest(2)
        await e.edit_text("ᴘɪɴɢɪɴɢ ✨")
        await rest(1)
        await e.edit_text(PING_TEXT.format(ping1, up, __version__), reply_markup=Button) 
       
    if m.from_user.id not in sudo:
        await m.reply(("ʏᴏᴜʀ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ ʜᴜʜ!!😏😏\nʙsᴅᴋ ɢᴀɴᴅ ᴘᴇ ɪᴛɴᴇ ᴛʜʜᴘᴀᴅ ᴍᴀʀᴜɴɢɪ ᴏᴡɴᴇʀ ɢɪʀɪ ᴄʜʜᴜᴛ ᴊᴀᴀʏᴇɢɪ ʜᴜʜ 🤭 [ʟᴏᴅᴀ](tg://user?id={}) ᴘᴇʀsᴏɴ.").format(sender.id))

# ------------------------------------------------------------------------------- #

PING_TEXT = """
˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ 🇮🇳 sʏsᴛᴇᴍ sᴛᴀᴛs :

**ᴘɪɴɢ ᴘᴏɴɢ:** `{}`
**ʙᴏᴛ ᴜᴘᴛɪᴍᴇ:** `{}`
**ʟɪʙʀᴀʀʏ:** `ᴘʏʀᴏɢʀᴀᴍ`
**ᴍʏ ᴍᴀsᴛᴇʀ: ** `sᴜᴍɪᴛ ʏᴀᴅᴀᴠ`
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `3.10.4`
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ:** `{}`
"""
# ------------------------------------------------------------------------------- #


Button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴄʟᴏsᴇ ๏",callback_data="close_data")
        ]
    ]
)


# ------------------------------------------------------------------------------- #




@Hiroko.on_message(filters.command("alive"))
async def alive(_,msg:Message):
    start_time = time.time()
    sender = msg.from_user
    up = get_readable_time((time.time() - tim))
    end_time = time.time()
    ping1 = str(round((end_time - start_time) * 1000, 3)) + " ms"    
    x = await msg.reply_photo(photo=random.choice(photo), caption="**ᴀʟɪᴠɪɴɢ....**")    
    await x.edit_caption("**๏ ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ɪs ᴀʟɪᴠᴇ ᴀɴᴅ ᴡᴏʀᴋɪɴɢ ɢᴏᴏᴅ ᴡɪᴛʜ ᴀ ᴘɪɴɢ ᴏғ :**  `{} ᴍs`\n**๏ ʙᴏᴛs sᴇʀᴠɪᴄᴇ ᴜᴘᴛɪᴍᴇ ɪs :** `{}`".format(ping1, up), reply_markup=Button)



# ------------------------------------------------------------------------------- #




