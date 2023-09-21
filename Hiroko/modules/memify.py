import os
import textwrap
from Hiroko import Hiroko
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message



@Hiroko.on_message(filters.command("mmf"))
async def memify_image(hiroko : Hiroko, message: Message):
    if not message.reply_to_message:
        await message.reply("Please reply to an image/sticker.")
        return

    reply_message = message.reply_to_message

    if not reply_message.media:
        await message.reply("Reply to an image/sticker.")
        return

    file_id = reply_message.media.file_id
    image = await hiroko.download_media(file_id)

    text = message.text.split("/mmf ", maxsplit=1)[1].strip()

    if not text:
        await message.reply("You must provide text to add to the image.")
        return

    await message.reply("Memifying this image! ✊🏻")

    meme = await draw_text(image, text)

    await message.reply_document(document=meme)

    os.remove(image)
    os.remove(meme)

async def draw_text(image_path, text):
    img = Image.open(image_path)
    i_width, i_height = img.size

    fnt = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    current_h, pad = 10, 5

    for u_text in textwrap.wrap(text, width=15):
        u_width, u_height = draw.textsize(u_text, font=fnt)

        draw.text(
            xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
            text=u_text,
            font=fnt,
            fill=(0, 0, 0),
        )

        draw.text(
            xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
            text=u_text,
            font=fnt,
            fill=(0, 0, 0),
        )

        draw.text(
            xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
            text=u_text,
            font=fnt,
            fill=(0, 0, 0),
        )

        draw.text(
            xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
            text=u_text,
            font=fnt,
            fill=(0, 0, 0),
        )

        draw.text(
            xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
            text=u_text,
            font=fnt,
            fill=(255, 255, 255),
        )

        current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(image_name)

    img.save(webp_file, "webp")

    return webp_file




