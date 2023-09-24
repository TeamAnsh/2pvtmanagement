import base64
import httpx
from Hiroko import Hiroko
from pyrogram import filters
import pyrogram
from uuid import uuid4
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import imghdr
import os
from asyncio import gather
from random import choice
from traceback import format_exc
from pyrogram.errors import (PeerIdInvalid, ShortnameOccupyFailed,
                             StickerEmojiInvalid, StickerPngDimensions,
                             StickerPngNopng, StickerTgsNotgs,
                             StickerVideoNowebm, UserIsBlocked)
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message
from Hiroko.Helper.sticker_help import *



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




async def get_file_size(file: Message):
    if file.photo:
        size = file.photo.file_size/1024
    elif file.document:
        size = file.document.file_size/1024
    elif file.video:
        size = file.video.file_size/1024
    elif file.audio:
        size = file.audio.file_size/1024
    elif file.sticker:
        size = file.sticker.file_size/1024
        
    if size <= 1024:
        return f"{round(size)} kb"
    elif size > 1024:
        size = size/1024
        if size <= 1024:
            return f"{round(size)} mb"
        elif size > 1024:
            size = size/1024
            return f"{round(size)} gb"

    



@Hiroko.on_message(filters.command(["stickerinfo","stinfo"]))
async def give_st_info(c: Hiroko , m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a sticker")
        return
    elif not m.reply_to_message.sticker:
        await m.reply_text("Reply to a sticker")
        return
    st_in = m.reply_to_message.sticker
    st_type = "Normal"
    if st_in.is_animated:
        st_type = "Animated"
    elif st_in.is_video:
        st_type = "Video"
    st_to_gib = f"""[Sticker]({m.reply_to_message.link}) info:
File ID : `{st_in.file_id}`
File name : {st_in.file_name}
File unique ID : `{st_in.file_unique_id}`
Date and time sticker created : `{st_in.date}`
Sticker type : `{st_type}`
Emoji : {st_in.emoji}
Pack name : {st_in.set_name}
"""
    kb = IKM([[IKB("➕ Add sticker to pack", url=f"https://t.me/addstickers/{st_in.set_name}")]])
    await m.reply_text(st_to_gib,reply_markup=kb)
    return

@Hiroko.on_message(filters.command(["stickerid","stid"]))
async def sticker_id_gib(c: Hiroko, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a sticker")
        return
    elif not m.reply_to_message.sticker:
        await m.reply_text("Reply to a sticker")
        return
    st_in = m.reply_to_message.sticker
    await m.reply_text(f"Sticker id: `{st_in.file_id}`\nSticker unique ID : `{st_in.file_unique_id}`")
    return


@Hiroko.on_message(filters.command(["kang", "steal"]))
async def kang(c:Hiroko, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("Reply to a sticker or image to kang it.")
    elif not (m.reply_to_message.sticker or m.reply_to_message.photo or (m.reply_to_message.document and m.reply_to_message.document.mime_type.split("/")[0]=="image")):
        return await m.reply_text("Reply to a sticker or image to kang it.")
    if not m.from_user:
        return await m.reply_text("You are anon admin, kang stickers in my pm.")
    msg = await m.reply_text("Kanging Sticker..")
    is_requ = False
    if m.reply_to_message.sticker:
        if m.reply_to_message.sticker.is_animated or m.reply_to_message.sticker.is_video:
            is_requ = True
    # Find the proper emoji
    args = m.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif m.reply_to_message.sticker:
        try:
          sticker_emoji = m.reply_to_message.sticker.emoji
        except Exception:
          ran = ["🤣", "😑", "😁", "👍", "🔥", "🙈", "🙏", "😍", "😘", "😱", "☺️", "🙃", "😌", "🤧", "😐", "😬", "🤩", "😀", "🙂", "🥹", "🥺", "🫥", "🙄", "🫡", "🫠", "🤫", "😓", "🥵", "🥶", "😤", "😡", "🤬", "🤯", "🥴", "🤢", "🤮", "💀", "🗿", "💩", "🤡", "🫶", "🙌", "👐", "✊", "👎", "🫰", "🤌", "👌", "👀", "💃", "🕺", "👩‍❤️‍💋‍👩", "👩‍❤️‍💋‍👨","👨‍❤️‍👨", "💑", "👩‍❤️‍👩", "👩‍❤️‍👨", "💏", "👨‍❤️‍💋‍👨", "😪", "😴", "😭", "🥸", "🤓", "🫤", "😮", "😧", "😲", "🥱", "😈", "👿", "🤖", "👾", "🙌", "🥴", "🥰", "😇", "🤣" ,"😂", "😜", "😎"]
          sticker_emoji = choice(ran)
    else:
        edit = await msg.reply_text("No emoji provided choosing a random emoji")
        ran = ["🤣", "😑", "😁", "👍", "🔥", "🙈", "🙏", "😍", "😘", "😱", "☺️", "🙃", "😌", "🤧", "😐", "😬", "🤩", "😀", "🙂", "🥹", "🥺", "🫥", "🙄", "🫡", "🫠", "🤫", "😓", "🥵", "🥶", "😤", "😡", "🤬", "🤯", "🥴", "🤢", "🤮", "💀", "🗿", "💩", "🤡", "🫶", "🙌", "👐", "✊", "👎", "🫰", "🤌", "👌", "👀", "💃", "🕺", "👩‍❤️‍💋‍👩", "👩‍❤️‍💋‍👨","👨‍❤️‍👨", "💑", "👩‍❤️‍👩", "👩‍❤️‍👨", "💏", "👨‍❤️‍💋‍👨", "😪", "😴", "😭", "🥸", "🤓", "🫤", "😮", "😧", "😲", "🥱", "😈", "👿", "🤖", "👾", "🙌", "🥴", "🥰", "😇", "🤣" ,"😂", "😜", "😎"]
        sticker_emoji = choice(ran)
        await edit.delete()
    await msg.edit_text(f"Makeing a sticker with {sticker_emoji} emoji")

    # Get the corresponding fileid, resize the file if necessary
    try:
        if is_requ or m.reply_to_message.photo or (m.reply_to_message.document and m.reply_to_message.document.mime_type.split("/")[0]=="image"):
            sizee = (await get_file_size(m.reply_to_message)).split()
            if (sizee[1] == "mb" and sizee > 10) or sizee[1] == "gb":
                await m.reply_text("File size is too big")
                return
            path = await m.reply_to_message.download()
            if not is_requ:
                try:
                    path = await resize_file_to_sticker_size(path)
                except OSError as e:
                    await m.reply_text(f"Error\n{e}")                   
                    os.remove(path)
                    return
    except Exception as e:
        await m.reply_text(f"Got an error:\n{e}")
        return
    try:
        if is_requ or not m.reply_to_message.sticker:
            # telegram doesn't allow animated and video sticker to be kanged as we do for normal stickers
            sticker = await create_sticker(
                await upload_document(
                    c, path, m.chat.id
                ),
                sticker_emoji
            )
            os.remove(path)
        elif m.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    m.reply_to_message.sticker.file_id
                ),
                sticker_emoji
            )
    except ShortnameOccupyFailed:
        await m.reply_text("Change Your Name Or Username")
        return

    except Exception as e:
        await m.reply_text(str(e))
        

    # Find an available pack & add the sticker to the pack; create a new pack if needed
    # Would be a good idea to cache the number instead of searching it every single time...
    kang_lim = 120
    st_in = m.reply_to_message.sticker
    st_type = "norm"
    is_anim = is_vid = False
    if st_in:
        if st_in.is_animated:
            st_type = "ani"
            kang_lim = 50
            is_anim = True
        elif st_in.is_video:
            st_type = "vid"
            kang_lim = 50
            is_vid = True
    packnum = 0
    limit = 0
    volume = 0
    packname_found = False
    
    try:
        while not packname_found:
            packname = f"CE{str(m.from_user.id)}{st_type}{packnum}_by_@HirokoRobot"
            kangpack = f"{('@'+m.from_user.username) if m.from_user.username else m.from_user.first_name[:10]} {st_type} {('vOl '+str(volume)) if volume else ''} by @{Config.BOT_USERNAME}"
            if limit >= 50: # To prevent this loop from running forever
                await m.reply_text("Failed to kang\nMay be you have made more than 50 sticker packs with me try deleting some")
                return
            sticker_set = await get_sticker_set_by_name(c,packname)
            if not sticker_set:
                sticker_set = await create_sticker_set(
                    client=c,
                    owner=m.from_user.id,
                    title=kangpack,
                    short_name=packname,
                    stickers=[sticker],
                    animated=is_anim,
                    video=is_vid
                )
            elif sticker_set.set.count >= kang_lim:
                packnum += 1
                limit += 1
                volume += 1
                continue
            else:
                try:
                    await add_sticker_to_set(c,sticker_set,sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            packname_found = True
        kb = IKM(
            [
                [
                    IKB("➕ Add Pack ➕",url=f"t.me/addstickers/{packname}")
                ]
            ]
        )
        await msg.delete()
        await m.reply_text(
            f"Kanged the sticker\nPack name: `{kangpack}`\nEmoji: {sticker_emoji}",
            reply_markup=kb
        )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = IKM(
            [[IKB("Start me first", url=f"t.me/{Config.BOT_USERNAME}")]]
        )
        await msg.delete()
        await m.reply_text(
            "You Need To Start A Private Chat With Me.",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await msg.delete()
        await m.reply_text(
            "Stickers must be png files but the provided image was not a png"
        )
    except StickerPngDimensions:
        await msg.delete()
        await m.reply_text("The sticker png dimensions are invalid.")
    except StickerTgsNotgs:
        await msg.delete()
        await m.reply_text("Sticker must be tgs file but the provided file was not tgs")
    except StickerVideoNowebm:
        await msg.delete()
        await m.reply_text("Sticker must be webm file but the provided file was not webm")
    except Exception as e:
        await msg.delete()
        await m.reply_text(f"Error occured\n{e}")
    return


@Hiroko.on_message(filters.command(["mmfb","mmfw","mmf"]))
async def memify_it(c: Hiroko, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Invalid type.")
        return
    rep_to = m.reply_to_message
    if not (rep_to.sticker or rep_to.photo or (rep_to.document and "image" in rep_to.document.mime_type.split("/"))):
        await m.reply_text("I only support memifying of normal sticker and photos for now")
        return
    if rep_to.sticker and (rep_to.sticker.is_animated or rep_to.sticker.is_video):
        await m.reply_text("I only support memifying of normal sticker and photos for now")
        return

    if len(m.command) == 1:
        await m.reply_text("Give me something to write")
        return
    filll = m.command[0][-1]
    if filll == "b":
        fiil = "black"
    else:
        fiil = "white"
    x = await m.reply_text("Memifying...")
    meme = m.text.split(None,1)[1].strip()
    name = f"Hiroko_{m.id}.png"
    path = await rep_to.download(name)
    is_sticker = False
    if rep_to.sticker:
        is_sticker = True
    output = await draw_meme(path,meme,is_sticker,fiil)
    await x.delete()
    xNx = await m.reply_photo(output[0])
    await xNx.reply_sticker(output[1])
    try:
        os.remove(output[0])
        os.remove(output[1])
    except Exception as e:
      print(f"error {e}")
      
       

@Hiroko.on_message(filters.command(["getsticker","getst"]))
async def get_sticker_from_file(c: Hiroko, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a sticker or file")
        return
    repl = m.reply_to_message
    if not (repl.sticker or repl.photo or (repl.document and repl.document.mime_type.split("/")[0]=="image")):
        await m.reply_text("I only support conversion of plain stickers and images for now")
        return
    if repl.sticker and (repl.sticker.is_video or repl.sticker.is_animated):
        await m.reply_text("I only support conversion of plain stickers for now")
        return
    x = await m.reply_text("Converting...")
    if repl.sticker:
        upp = await repl.download()
        up = toimage(upp,is_direc=True)
        await x.delete()
        await m.reply_photo(up)
        os.remove(up)
        return
    elif repl.photo:
        upp = await repl.download()
        up = tosticker(upp,is_direc=True)
        await x.delete()
        await m.reply_sticker(up)
        os.remove(up)
        return

        
