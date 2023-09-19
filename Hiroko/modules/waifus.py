from config import SUDO_USERS
from pyrogram import Client, filters
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyromod import listen
from pyrogram.types import Message
from Hiroko import Hiroko

# Initialize MongoDB connection
mongo = MongoCli(MONGO_URL).Rankings
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]



# Define a dictionary to store user states
user_states = {}

# Command handler for /addwaifu (only for sudo users)
@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifu_start(client, message):
    user_id = message.from_user.id
    user_states[user_id] = {}
    
    await message.reply_text("🌟 Great! Let's add a new waifu. Please send the waifu's photo as a reply to this message.")
    user_states[user_id]["state"] = "waiting_for_photo"
    
    # Use ask to wait for the photo input
    user_states[user_id]["ask"] = await message.ask("Send the waifu's photo now.", reply_to=message)

# Message handler for user input during the /addwaifu process
@Hiroko.on_message(filters.private)
async def handle_user_input(client, message):
    user_id = message.from_user.id
    if user_id in user_states:
        user_state = user_states[user_id]["state"]
        if user_state == "waiting_for_photo":
            if message.photo:
                # Store the photo file ID
                user_states[user_id]["photo"] = message.photo[-1].file_id
                user_states[user_id]["state"] = "waiting_for_name"
                
                # Use ask to wait for the name input
                user_states[user_id]["ask"] = await message.ask("Thanks! Now, please enter the waifu's name.")
            else:
                await message.reply_text("Please send a photo as a reply.")
        elif user_state == "waiting_for_name":
            user_states[user_id]["name"] = message.text
            user_states[user_id]["state"] = "waiting_for_anime"
            
            # Use ask to wait for the anime input
            user_states[user_id]["ask"] = await message.ask("Got it! Please enter the anime the waifu is from.")
        elif user_state == "waiting_for_anime":
            user_states[user_id]["anime"] = message.text
            user_states[user_id]["state"] = "waiting_for_rarity"
            
            # Use ask to wait for the rarity input
            user_states[user_id]["ask"] = await message.ask("Great! Finally, please enter the rarity of the waifu (e.g., common, rare, legendary).")
        elif user_state == "waiting_for_rarity":
            user_states[user_id]["rarity"] = message.text
            
            # Insert the waifu data into the MongoDB collection
            waifu_data = {
                "photo": user_states[user_id]["photo"],
                "name": user_states[user_id]["name"],
                "anime": user_states[user_id]["anime"],
                "rarity": user_states[user_id]["rarity"],
            }
            await waifu_collection.insert_one(waifu_data)
            
            # Clean up user state
            del user_states[user_id]
            
            await message.reply_text("🌟 Waifu added successfully! 🌟")





