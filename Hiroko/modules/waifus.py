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




@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
    if len(message.command) < 2:
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo-name-anime-rarity")
    waifu_text = message.text.split(None, 1)[1]
    waifu = waifu_text.split("-")
    if len(waifu) != 5:
        return await message.reply("❌ Invalid format. Please provide waifu details in the format: /addwaifu photo-name-anime-rarity")

    waifu_photo_url, waifu_name, waifu_anime, waifu_rarity, waifu_prize = waifu

    response = requests.get(waifu_photo_url)
    if response.status_code != 200:
        return await message.reply("❌ Failed to download the image from the URL.")

    waifu_photo_bytes = BytesIO(response.content)

    waifu_data = {
        "waifu_photo": waifu_photo_bytes.getvalue(),  # Store as bytes
        "waifu_name": waifu_name,
        "waifu_anime": waifu_anime,
        "waifu_rarity": waifu_rarity,
        "waifu_prize": waifu_prize,
    }

    await waifu_collection.insert_one(waifu_data)

    await Hiroko.send_photo(chat_id=-1001936480103, photo=waifu_photo_bytes, reply_markup=InlineKeyboardMarkup([       
    [  
        InlineKeyboardButton(f"{message.from_user.first_name}", url=f"https://t.me/{message.from_user.username}"),
    ],
    [
        InlineKeyboardButton("close", callback_data="maintainer_"),
    ]]))
    await message.reply_text("🌟 Waifu added successfully! 🌟")


# ======================================================================= #
"""
chat_count = {}

@Hiroko.on_message(filters.group, group=69)
async def waifu_sender(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in chat_count:
        chat_count[chat_id] = {'count': 0}
    chat_count[chat_id]['count'] += 1
    
    if chat_count[chat_id]['count'] == 10:
        
        photo = await waifu_collection.find({"waifu_photo" : waifu_photo})         
        image = random.choice(photo)
        await Hiroko.send_photo(
            message.chat.id,
            photo=image,
            caption=f"Wew sexy Waifu Appeared !!!\n\nGuess Her Name And Make Her Your waifu By Using Spell /grab [Her Name]!"
        )
        chat_count.pop(chat_id)
"""

# ==================================================================== #
@Hiroko.on_message(filters.command("grab", prefixes="/"))
async def grab_waifus(client, message):
    if len(message.command) != 2:
        return await message.reply("Hello sweetheart. Please use /grab waifu_name")

    user_id = message.from_user.id
    waifu_name = message.command[1]
    waifus_name = await waifu_collection.find({"waifu_name" : waifu_name})

    if waifu_name in waifus_name:
        user_waifu_data = {
            "user_id": user_id,
            "waifu": waifu_name
        }
        await waifu_collection.insert_one(user_waifu_data)
        await message.reply(f"Grabbed {waifu_name} as your waifu!")
    else:
        await message.reply("bsdk k glt hai name . Please choose a valid waifu.")




# Command: /mywaifus
@Hiroko.on_message(filters.command("mywaifus", prefixes="/") & filters.private)
async def my_waifus(_, message):
    user_id = message.from_user.id
    user_waifus = await waifu_collection.find({"user_id": user_id}).to_list(None)
    
    if user_waifus:
        waifus = "\n".join([waifu["waifu_name"] for waifu in user_waifus])
        await message.reply(f"👫 Your waifus:\n{waifus}")
    else:
        await message.reply("👫 You don't have any waifus yet. Use /grab to get one!")


@Hiroko.on_message(filters.command("giftwaifu", prefixes="/") & filters.private)
async def gift_waifu(_, message):
    if len(message.command) != 2:
        return await message.reply("🎁 Please use /giftwaifu @user to gift a waifu.")
    
    user_id = message.from_user.id
    target_username = message.command[1]
    
    waifu_to_gift = await waifu_collection.find_one({"user_id": user_id})
    
    if waifu_to_gift:
        await waifu_collection.update_one({"user_id": user_id}, {"$unset": {"user_id": ""}})
        await message.reply(f"🎁 You've gifted {waifu_to_gift['waifu_name']} to {target_username}!")
    else:
        await message.reply("🎁 You don't have any waifus to gift.")




