import requests
import asyncio
import matplotlib.pyplot as plt
from io import BytesIO
from config import SUDO_USERS, MONGO_URL
from pyrogram import *
from pyrogram.types import *
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from Hiroko import Hiroko
import random
import psycopg2
from Hiroko.SQL import DB, cusr
import json

mongo = MongoCli(MONGO_URL)
db = mongo["waifu_bot"]
waifu_collection = db["waifus"]
users_collection = db["users"]

DICT = {}
trade_requests = {}
chat_count = {}

cusr.execute("""
    CREATE TABLE IF NOT EXISTS waifus (
        id SERIAL PRIMARY KEY,
        photo TEXT NOT NULL,
        name TEXT NOT NULL,
        anime TEXT NOT NULL,
        rarity TEXT NOT NULL
    )
""")
DB.commit()
# ==================================================================== #

@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifus(_, message):
    if len(message.text) < 10:
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo-name-anime-rarity")
    if not message.text.split(maxsplit=1)[1]:
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo-name-anime-rarity")
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split("+")
    if not data[0].startswith("https"):
        return await message.reply("link de bhai pic ka")
    if not data[1]:
        return await message.reply("naam bol bhai bandi ka")
    if not data[2]:
        return await message.reply_text("anime ka naam bol mosquitochod")
    if not data[3]:
        return await message.reply("rarity bol madarchod")
    
    photo = data[0]
    nam = data[1]
    ani = data[2]
    rare = data[3]
    levels = ["common", "rare", "epic",  "legendary","royal"]
    if data[3].lower() not in levels:
        return await message.reply("Invalid Rarity")
    rarity = rare.title()
    anime = ani.title()
    name = nam.title()
    try:
        cusr.execute(
            "INSERT INTO waifus (photo, name, anime, rarity) VALUES (%s, %s, %s, %s)",
            (photo, name, anime, rarity)
        )
        DB.commit()
    except Exception as e:
        await Hiroko.send_message(-1001946875647 , str(e))
        return await message.reply("Falied Check Format Again")
    await message.reply_photo(photo=photo,caption="🌟 Waifu added successfully! 🌟")
    


# ======================================================================= #


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




# ==================================================================== #

@Hiroko.on_message(filters.command("mywaifus", prefixes="/") & filters.private)
async def my_waifus(_, message):
    user_id = message.from_user.id
    user_waifus = await waifu_collection.find({"user_id": user_id}).to_list(None)
    
    if user_waifus:
        waifus = "\n".join([waifu["waifu_name"] for waifu in user_waifus])
        await message.reply(f"👫 Your waifus:\n{waifus}")
    else:
        await message.reply("👫 You don't have any waifus yet. Use /grab to get one!")


# ==================================================================== #

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


# ==================================================================== #

@Hiroko.on_message(filters.command("trade", prefixes="/"))
async def trade_waifus(_, message):
    user_id = message.from_user.id
    await message.reply("Mention the user you want to trade with in the format: `/trade @username waifu_name`")
    
    @Hiroko.on_message(filters.reply & filters.user(user_id))
    async def confirm_trade(_, trade_message):
        if trade_message.text.startswith("/trade @") and " " in trade_message.text:
            parts = trade_message.text.split()
            if len(parts) == 3:
                target_username = parts[1].replace("@", "")
                waifu_name = parts[2]
                
                
                target_user = await Hiroko.get_users(target_username)
                if not target_user:
                    await message.reply("The target user doesn't exist.")
                    return
                
                
                user_data = await users_collection.find_one({"user_id": user_id})
                if not user_data or waifu_name not in user_data.get("waifus", []):
                    await message.reply("You don't have the specified waifu to trade.")
                    return
                
                
                trade_request_id = str(message.message_id)
                
                
                trade_requests[trade_request_id] = {
                    "user_id": user_id,
                    "target_user_id": target_user.id,
                    "waifu_name": waifu_name,
                }
                
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Accept", callback_data=f"accept_trade_{trade_request_id}"),
                     InlineKeyboardButton("Decline", callback_data=f"decline_trade_{trade_request_id}")]
                ])
                
                await message.reply(f"@{target_username}, {message.from_user.mention} wants to trade {waifu_name} with you.", reply_markup=keyboard)
            else:
                await message.reply("Invalid format. Use `/trade @username waifu_name`.")
        else:
            await message.reply("Invalid format. Use `/trade @username waifu_name`.")
    
    await asyncio.sleep(60)  # Wait for 60 seconds for a reply
    await message.reply("Trade request expired.")


# ==================================================================== #

@Hiroko.on_callback_query(filters.regex(r"^accept_trade_(\d+)$"))
async def accept_trade(_, callback_query):
    trade_request_id = callback_query.matches[0].group(1)
    
    if trade_request_id in trade_requests:
        trade_request = trade_requests.pop(trade_request_id)
        target_user_id = trade_request["target_user_id"]
        user_id = trade_request["user_id"]
        waifu_name = trade_request["waifu_name"]
        
        
        await users_collection.update_one({"user_id": user_id}, {"$pull": {"waifus": waifu_name}})
        await users_collection.update_one({"user_id": target_user_id}, {"$push": {"waifus": waifu_name}})
        
        await callback_query.message.edit_text(f"Trade accepted! {callback_query.from_user.mention} has traded {waifu_name} with you.")
    
    else:
        await callback_query.answer("Trade request not found or expired.", show_alert=True)



@Hiroko.on_callback_query(filters.regex(r"^decline_trade_(\d+)$"))
async def decline_trade(_, callback_query):
    trade_request_id = callback_query.matches[0].group(1)
    
    if trade_request_id in trade_requests:
        trade_requests.pop(trade_request_id)
        await callback_query.message.edit_text(f"Trade declined. {callback_query.from_user.mention} has declined the trade request.")
    
    else:
        await callback_query.answer("Trade request not found or expired.", show_alert=True)

# ==================================================================== #




chat_groups_data = [
    {"group_name": "Group 1", "percentage": 15},
    {"group_name": "Group 2", "percentage": 12},
    {"group_name": "Group 3", "percentage": 10},
    {"group_name": "Group 4", "percentage": 8},
    {"group_name": "Group 5", "percentage": 5},
]


@Hiroko.on_message(filters.command("topgrabber", prefixes="/"))
async def view_top_grabbers(_, message):
    top_players = await users_collection.find().sort([("waifus_collected", -1)]).limit(10).to_list(None)
    
    player_names = [user.get("username", "Unknown") for user in top_players]
    waifus_collected = [user.get("waifus_collected", 0) for user in top_players]
    
    plt.figure(figsize=(10, 6))
    plt.barh(player_names, waifus_collected, color='skyblue')
    plt.xlabel('Waifus Collected')
    plt.title('Top 10 Waifu Players')
    
    caption = "Top 10 Waifu Players:\n"
    for i, player_name in enumerate(player_names, start=1):
        caption += f"{i}. {player_name}\n"
    
    chart_image = 'top_waifu_players.png'
    plt.savefig(chart_image, bbox_inches='tight')
    plt.close()
    await message.reply_photo(photo=chart_image, caption=caption)
    

    import os
    os.remove(chart_image)


@Hiroko.on_message(filters.command("topgrabbersgroups", prefixes="/"))
async def view_top_groups(_, message):
    group_names = [data["group_name"] for data in chat_groups_data]
    percentages = [data["percentage"] for data in chat_groups_data]
    

    plt.figure(figsize=(8, 6))
    plt.bar(group_names, percentages, color='red')
    plt.ylabel('Percentage')
    plt.title('Top 5 Chat Groups by Percentage')
    
    
    for i, percentage in enumerate(percentages):
        plt.text(i, percentage + 1, f"{percentage}%", ha='center', va='bottom')
    

    chart_image = 'top_chat_groups.png'
    plt.savefig(chart_image, bbox_inches='tight')
    plt.close()
    await message.reply_photo(photo=chart_image, caption="Top 5 Chat Groups by Percentage")

    import os
    os.remove(chart_image)



