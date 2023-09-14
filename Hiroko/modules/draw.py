import asyncio
import time
from Hiroko import Hiroko
from pyrogram import Client, filters
from lexica.core_async import AsyncClient
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


client = AsyncClient()

async def gen_image(prompt: str, negative_prompt: str = None, model_id: int = 2, timeout: int = 100) -> dict:
    task = await client.generate(model_id, prompt=prompt, negative_prompt=negative_prompt)

    start = time.time()
    while time.time() - start < timeout:
        r = await client.getImages(task["task_id"], task["request_id"])
        if r["code"] == 2:
            return r['img_urls']

        await asyncio.sleep(4)
    return



button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")
        ]
    ]
)



@Hiroko.on_message(filters.command("nx"))
async def draw(_, msg):
    if len(msg.command) < 2:
        return await msg.reply_text("<code>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ. ᴜsᴀɢᴇ: /nx &lt;prompt&gt;</code>")
    
    prompt = msg.command[1]
    
    process_msg = await msg.reply_text("ᴡᴀɪᴛᴏ...")
    images = await gen_image(prompt) 
    
    if not images:
        return await process_msg.edit_text("<code>ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. ᴘʟᴇᴀᴀᴇ ᴛʀʏ ᴀɢᴀɪɴ.</code>")  
    
    for image in images:
        await process_msg.edit_text("**ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ ᴅʀᴀᴡɪɴɢ...**")
        await asyncio.sleep(2)
        await process_msg.edit_text("**ɢɪᴠɪɴɢ sᴏᴍᴇ ғɪɴɪsʜɪɴɢ ᴛᴏᴜᴄʜᴇs...**")
        await asyncio.sleep(2)
        await process_msg.edit_text("**ʏᴏᴜ ᴅʀᴀᴡɪɴɢ ɪs ʀᴇᴀᴅʏ! 🎨\nɴᴏᴡ ᴜᴘʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ᴅʀᴀᴡɪɴɢ...**")
        await asyncio.sleep(2)
        await process_msg.delete()
        await asyncio.sleep(1)
        await Hiroko.send_photo(msg.chat.id, image, reply_markup=button)




