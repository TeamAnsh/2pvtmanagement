import os
from Hiroko import Hiroko
from pyrogram import filters
from pyrogram.types import Message



downloads_directory = os.path.join("Hiroko", "Helper", "downloader", "downloads")
raw_directory = os.path.join("Hiroko", "Helper", "downloader", "raw_files")


@Hiroko.on_message(filters.command(["rmd", "clear"], prefixes=["/", "!"]))
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads_directory)
    if ls_dir:
        for file in os.listdir(downloads_directory):
            os.remove(os.path.join(downloads_directory, file))
        await message.reply_text("✅ **Deleted all download files**")
    else:
        await message.reply_text("❌ **No files downloaded**")


@Hiroko.on_message(filters.command(["rmw", "clean"], prefixes=["/", "!"]))
async def clear_raw(_, message: Message):
    ls_dir = os.listdir(raw_directory)
    if ls_dir:
        for file in os.listdir(raw_directory):
            os.remove(os.path.join(raw_directory, file))
        await message.reply_text("✅ **Deleted all raw files**")
    else:
        await message.reply_text("❌ **No raw files**")


@Hiroko.on_message(filters.command(["cleanup"], prefixes=["/", "!"]))
async def cleanup(_, message: Message):
    pth = os.path.realpath(".")
    ls_files = os.listdir(pth)
    if ls_files:
        for dta in os.listdir(pth):
            if dta.endswith(".webm") or dta.endswith(".jpg"):
                os.remove(os.path.join(pth, dta))
        await message.reply_text("✅ **Cleaned**")
    else:
        await message.reply_text("✅ **Already cleaned**")





