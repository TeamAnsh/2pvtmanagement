import os
from Hiroko import Hiroko
from pyrogram import filters
from pyrogram.types import Message

downloads = os.path.realpath("downloads")
raw_files = os.path.realpath("raw_files")

@Hiroko.on_message(filters.command(["rmd", "clear"], prefixes=["/", "!"]))
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("✅ **ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇs**")
    else:
        await message.reply_text("❌ **ɴᴏ ғɪʟᴇs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ**")

        
@Hiroko.on_message(filters.command(["rmw", "clean"], prefixes=["/", "!"]))
async def clear_raw(_, message: Message):
    ls_dir = os.listdir(raw_files)
    if ls_dir:
        for file in os.listdir(raw_files):
            os.remove(os.path.join(raw_files, file))
        await message.reply_text("✅ **ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ʀᴀᴡ ғɪʟᴇs**")
    else:
        await message.reply_text("❌ **ɴᴏ ʀᴀᴡ ғɪʟᴇs**")


@Hiroko.on_message(filters.command(["cleanup"], prefixes=["/", "!"]))
async def cleanup(_, message: Message):
    pth = os.path.realpath(".")
    ls_dir = os.listdir(pth)
    if ls_dir:
        for dta in os.listdir(pth):
            os.system("rm -rf *.webm *.jpg")
        await message.reply_text("✅ **ᴄʟᴇᴀɴᴇᴅ**")
    else:
        await message.reply_text("✅ **ᴀʟʀᴇᴀᴅʏ ᴄʟᴇᴀɴᴇᴅ**")



