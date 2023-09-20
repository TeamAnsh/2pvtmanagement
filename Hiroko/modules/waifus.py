from config import SUDO_USERS
from pyrogram import filters
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram.types import Message
from Hiroko import Hiroko


mongo = MongoCli(MONGO_URL).Rankings
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]





@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
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
    await message.reply_text("🌟 Waifu added successfully! 🌟")


