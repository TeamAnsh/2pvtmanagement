from config import SUDO_USERS
from pyrogram import Client, filters
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyromod import listen
from pyrogram.types import Message
from Hiroko import Hiroko


mongo = MongoCli(MONGO_URL).Rankings
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]





@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
    user_id = message.from_user.id    
    waifu_photo = await message.chat.ask("🌟 Great! Let's add a new waifu. Please send the waifu's photo as a reply to this message.")
    photo = waifu_photo.photo[-1].file_id
    waifu_name = await message.chat.ask("Thanks! Now, please enter the waifu's name.")
    name = waifu_name.text
    anime_name = await message.chat.ask("Got it! Please enter the anime the waifu is from.")
    anime = anime_name.text
    waifu_rarity = await message.chat.ask("Great! Finally, please enter the rarity of the waifu (e.g., common, rare, legendary).") 
    rarity = waifu_rarity.text
    waifu_data = {
        "waifu_photo": photo,
        "waifu_name": name,
        "waifu_anime": anime,
        "waifu_rarity": rarity,
    }
    await waifu_collection.insert_one(waifu_data)            
    await message.reply_text("🌟 Waifu added successfully! 🌟")



