import requests
import asyncio
from Hiroko import Hiroko
from pyrogram.types import Message
from pyrogram import Client, filters

 

            
@Hiroko.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await Hiroko.send_message(message.chat.id, "waito...")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await Hiroko.send_message(message.chat.id, "waito..")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()



