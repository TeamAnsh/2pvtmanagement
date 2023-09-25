import base64
import httpx
from Hiroko import Hiroko
from pyrogram import filters
import pyrogram
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


@Hiroko.on_message(filters.reply & filters.command("upscale"))
async def upscale_image(client, message):
    try:
        # Check if the replied message contains a photo
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("Please reply to an image to upscale it.")
            return

        # Access the image file_id from the replied message
        image = message.reply_to_message.photo.file_id
        file_path = await client.download_media(image)

        with open(file_path, "rb") as image_file:
            f = image_file.read()

        b = base64.b64encode(f).decode("utf-8")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.qewertyy.me/upscale", data={"image_data": b}, timeout=None
            )

        # Save the upscaled image
        with open("upscaled_image.png", "wb") as output_file:
            output_file.write(response.content)

        # Send the upscaled image as a PNG file
        await client.send_document(
            message.chat.id,
            document="upscaled_image.png",
            caption="Here is the upscaled image!",
        )

    except Exception as e:
        print(f"Failed to upscale the image: {e}")
        await message.reply_text("Failed to upscale the image. Please try again later.")
        # You may want to handle the error more gracefully here




@Hiroko.on_message(filters.command("packkang"))
async def _packkang(app :Hiroko,message):  
    txt = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ....")
    if not message.reply_to_message:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ')
        return
    if not message.reply_to_message.sticker:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ')
        return
    if message.reply_to_message.sticker.is_animated or  message.reply_to_message.sticker.is_video:
        return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɴᴏɴ-ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ")
    if len(message.command) < 2:
        pack_name =  f'{message.from_user.first_name}_sticker_pack_by_@HirokoRobot'
    else :
        pack_name = message.text.split(maxsplit=1)[1]
    short_name = message.reply_to_message.sticker.set_name
    stickers = await app.invoke(
        pyrogram.raw.functions.messages.GetStickerSet(
            stickerset=pyrogram.raw.types.InputStickerSetShortName(
                short_name=short_name),
            hash=0))
    shits = stickers.documents
    sticks = []
    
    for i in shits:
        sex = pyrogram.raw.types.InputDocument(
                id=i.id,
                access_hash=i.access_hash,
                file_reference=i.thumbs[0].bytes
            )
        
        sticks.append(
            pyrogram.raw.types.InputStickerSetItem(
                document=sex,
                emoji=i.attributes[1].alt
            )
        )

    try:
        short_name = f'stikcer_pack_{str(uuid4()).replace("-","")}_by_{app.me.username}'
        user_id = await app.resolve_peer(message.from_user.id)
        await app.invoke(
            pyrogram.raw.functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=short_name,
                stickers=sticks,
            )
        )
        await txt.edit(f"𝙿𝙰𝙲𝙺 [𝙺𝙰𝙽𝙶𝙴𝙳](http://t.me/addstickers/{short_name})!\n𝚃𝙾𝚃𝙰𝙻 𝚂𝚃𝙸𝙲𝙺𝙴𝚁: {len(sticks)}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴘᴀᴄᴋ ʟɪɴᴋ",url=f"http://t.me/addstickers/{short_name}")]]))
    except Exception as e:
        await message.reply(str(e))
