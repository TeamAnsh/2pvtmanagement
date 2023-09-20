from config import SUDO_USERS
from pyrogram import filters
from pyrogram.types import *
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram.types import Message
from Hiroko import Hiroko


mongo = MongoCli(MONGO_URL).Rankings
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]

button = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"message.from_user.mention", url=f"message.from_user.username"),
            InlineKeyboardButton("close", callback_data="maintainer_"),
        ]                
    ])



@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
    if len(message.command) < 2:
        return await message.reply("💌 **hello hottie ..**")

    waifu = message.text.split("-")
    waifu_photo = waifu[0]
    waifu_name = waifu[1]
    waifu_anime = waifu[2]
    waifu_rarity = waifu[3]
    waifu_data = {
        "waifu_photo": waifu_photo,
        "waifu_name": waifu_name,
        "waifu_anime": waifu_anime,
        "waifu_rarity": waifu_rarity,
    }
    await waifu_collection.insert_one(waifu_data)
    await Hiroko.send_photo(-1001936480103, photo=waifu_photo, reply_markup=button)
    await message.reply_text("🌟 Waifu added successfully! 🌟")

