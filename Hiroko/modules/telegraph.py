import os
from telegraph import upload_file
from Hiroko import Hiroko
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Hiroko.on_message(filters.command(["tg", "tgm", "telegraph"], prefixes=["/", "!"]))
async def telegraph_command(_, message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ ғɪʟᴇ.**")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply_text("**ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇ ғᴏʀᴍᴀᴛ !**")
        return
    download_location = await Hiroko.download_media(
        message=message.reply_to_message, file_name="root/nana/"
    )
    try:
        response = upload_file(download_location)
        buttons = [
            [
                InlineKeyboardButton(
                    "ᴛᴇʟᴇɢʀᴀᴘʜ", url=f"https://telegra.ph{response[0]}"
                ),
                InlineKeyboardButton(
                    "sʜᴀʀᴇ",
                    url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}",
                ),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            f"**ʜᴇʟʟᴏ {message.from_user.mention}!**\n**ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ:** [🌿](https://telegra.ph{response[0]})",
            reply_markup=reply_markup,
        )
    except Exception as err:
        await Hiroko.send_message(message.chat.id, f"**ᴇʀʀᴏʀ**: {err}")
    finally:
        os.remove(download_location)



