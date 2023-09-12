import os
from telegraph import upload_file
from Hiroko import Hiroko
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["tg", "tgm", "telegraph"], prefixes=["/", "!"]))
async def telegraph(client: Client, message: Message):
    get_me = await client.get_me()
    USERNAME = get_me.username
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("reply to a supported media file")
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
        await message.reply_text("not supported!")
        return
    download_location = await client.download_media(
        message=message.reply_to_message, file_name="root/nana/"
    )
    try:
        response = upload_file(download_location)
        buttons = [        
            [            
                InlineKeyboardButton("๏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ๏", url=f"https://telegra.ph{response[0]}"), 
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/TheNixaSupport")           
            ]        
        ]
        reply_markup = InlineKeyboardMarkup(buttons)            
        await message.reply_text("**ʜᴇʟʟᴏ [{}](tg://user?id={})**\n**ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴊᴜsᴛ ᴛᴀᴘ ᴛᴇʟᴇɢʀᴀᴘʜ ʙᴜᴛᴛᴏɴ ʟɪɴᴋ ᴀɴᴅ ᴄᴏᴘʏ**".format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    except Exception as document:
        await client.send_message(message.chat.id, document)
    finally:
        os.remove(download_location)
        
# ------------------------------------------------------------------------------- #

