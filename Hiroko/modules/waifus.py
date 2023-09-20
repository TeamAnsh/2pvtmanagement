import requests
from io import BytesIO
from config import SUDO_USERS, MONGO_URL
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from Hiroko import Hiroko


mongo = MongoCli(MONGO_URL)
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]

button = InlineKeyboardMarkup([       
    [  
        InlineKeyboardButton(f"message.from_user.mention", url=f"https://t.me/@{message.from_user.username}"),
        InlineKeyboardButton("Close", callback_data="maintainer_"),
    ]
])



@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
    if len(message.command) < 2:
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo-name-anime-rarity")
    waifu_text = message.text.split(None, 1)[1]
    waifu = waifu_text.split("-")
    if len(waifu) != 4:
        return await message.reply("❌ Invalid format. Please provide waifu details in the format: /addwaifu photo-name-anime-rarity")

    waifu_photo_url, waifu_name, waifu_anime, waifu_rarity = waifu

    response = requests.get(waifu_photo_url)
    if response.status_code != 200:
        return await message.reply("❌ Failed to download the image from the URL.")

    waifu_photo_bytes = BytesIO(response.content)

    waifu_data = {
        "waifu_photo": waifu_photo_bytes.getvalue(),  # Store as bytes
        "waifu_name": waifu_name,
        "waifu_anime": waifu_anime,
        "waifu_rarity": waifu_rarity,
    }

    await waifu_collection.insert_one(waifu_data)

    await Hiroko.send_photo(chat_id=-1001936480103, photo=waifu_photo_bytes, reply_markup=button)
    await message.reply_text("🌟 Waifu added successfully! 🌟")



