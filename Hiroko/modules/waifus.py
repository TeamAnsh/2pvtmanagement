from config import SUDO_USERS
from pyrogram import Client, filters
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyromod import listen
from Hiroko import Hiroko


mongo = MongoCli(MONGO_URL).Rankings
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]



# Define a dictionary to store user states
user_states = {}

# Command handler for /addwaifu (only for sudo users)
@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
@listen()
async def add_waifu_start(client, message):
    user_id = message.from_user.id
    user_states[user_id] = "waiting_for_photo"
    
    await message.reply_text("🌟 Great! Let's add a new waifu. Please send the waifu's photo as a reply to this message.")

# Message handler for user input during the /addwaifu process
@Hiroko.on_message(filters.photo & filters.private)
@listen()
async def handle_user_input(client, message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)

    if user_state == "waiting_for_photo":
        user_states[user_id] = "waiting_for_name"
        user_states[user_id + "_photo"] = message.photo[-1].file_id
        
        await message.reply_text("📸 Thanks! Now, please enter the waifu's name.")
    elif user_state == "waiting_for_name":
        user_states[user_id] = "waiting_for_anime"
        user_states[user_id + "_name"] = message.text
        
        await message.reply_text("✅ Got it! Please enter the anime the waifu is from.")
    elif user_state == "waiting_for_anime":
        user_states[user_id] = "waiting_for_rarity"
        user_states[user_id + "_anime"] = message.text
        
        await message.reply_text("🎉 Great! Finally, please enter the rarity of the waifu (e.g., common, rare, legendary).")
    elif user_state == "waiting_for_rarity":
        user_states.pop(user_id, None)
        photo = user_states.pop(user_id + "_photo", None)
        name = user_states.pop(user_id + "_name", None)
        anime = user_states.pop(user_id + "_anime", None)
        
        if photo and name and anime:
            waifu_data = {
                "photo": photo,
                "name": name,
                "anime": anime,
                "rarity": message.text,
            }
            await waifu_collection.insert_one(waifu_data)

            await message.reply_text("🌟 Waifu added successfully! 🌟")



