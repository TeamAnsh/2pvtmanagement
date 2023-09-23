import requests, asyncio, random, psycopg2, json
import matplotlib.pyplot as plt
from io import BytesIO
from config import SUDO_USERS
from pyrogram import *
from pyrogram.types import *
from Hiroko import Hiroko
from Hiroko.SQL import DB, cusr



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
cusr.execute("""
    CREATE TABLE IF NOT EXISTS grabbed (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
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
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo+name-anime+rarity")
    if not message.text.split(maxsplit=1)[1]:
        return await message.reply("💌 Hello hottie, please provide the waifu details in the format: /addwaifu photo+name+anime+rarity")
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
        return await message.reply("**ᴅᴇᴛᴇᴄᴛᴇᴅ ɪɴᴠᴀʟɪᴅ ʀᴀʀɪᴛʏ.**")
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
        print(f"Error {e}")
        return await message.reply("**ғᴀʟɪᴇᴅ ᴄʜᴇᴄᴋ ғᴏʀᴍᴀᴛ ᴀɢᴀɪɴ.**")
    await message.reply_photo(photo=photo,caption="**ᴡᴀɪғᴜ ᴀᴅᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ ʏᴏᴜʀ ᴡᴀɪғᴜs ᴅᴀᴛᴀʙᴀsᴇ.🎉**")
    await Hiroko.send_photo(-1001936480103, photo=photo, reply_markup=InlineKeyboardMarkup([[
     InlineKeyboardButton(f"{message.from_user.first_name}", url=f"https://t.me/{message.from_user.username}"),    
      ]]))
    await Hiroko.send_message(-1001946875647, text=f"**ᴡᴀɪғᴜ ᴜᴘʟᴏᴀᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴇᴄᴋ ᴡᴀɪғᴜs ᴅᴏᴍᴀɪɴ**[🎉]({photo}) @WaifusDomain", reply_markup=InlineKeyboardMarkup([[
     InlineKeyboardButton(f"{message.from_user.first_name}", url=f"https://t.me/{message.from_user.username}"),    
      ]]))

    
    


# ======================================================================= #


@Hiroko.on_message(filters.group, group=11)
async def _watcher(_, message):
    chat_id = message.chat.id
    if not message.from_user:
        return
    if chat_id not in DICT:
        DICT[chat_id] = {'count': 0, 'running_count': 0, 'photo': None, 'name': None, 'anime': None, 'rarity': None}
    DICT[chat_id]['count'] += 1

    if DICT[chat_id]['count'] == 100:
        cusr.execute("SELECT * FROM waifus")
        result = cusr.fetchall()
        waifu = random.choice(result)
        photo = waifu[1]
        name = waifu[2]
        anime = waifu[3]
        rarity = waifu[4]
        try:
            msg = await _.send_photo(chat_id, photo=photo, caption="**ᴡᴇᴡ ᴀ sᴇxʏ ᴡᴀɪғᴜ ᴀᴘᴘᴇᴀʀᴅᴇᴅ ᴀᴅᴅ ʜᴇʀ ᴛᴏ ʏᴏᴜʀ ᴡᴀɪғᴜ ʟɪsᴛ ʙʏ sᴇɴᴅɪɴɢ: <code>/grab</code> ᴡᴀɪғᴜ ɴᴀᴍᴇ**")
            DICT[chat_id]['photo'] = photo
            DICT[chat_id]['name'] = name
            DICT[chat_id]['anime'] = anime
            DICT[chat_id]['rarity'] = rarity
            run.clear()
        except errors.FloodWait as e:
            await asyncio.sleep(e.value)

    if DICT[chat_id]['name']:
        DICT[chat_id]['running_count'] += 1
        if DICT[chat_id]['running_count'] == 30:
            try:
                character = DICT[chat_id]['name']
                await _.send_message(chat_id, f"**ᴀ sᴇxʏ ᴡᴀɪғᴜ ʜᴀꜱ ʀᴀɴ ᴀᴡᴀʏ!!**\n\n**ɴᴀᴍᴇ** <code>{character}</code>\n**ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ʀᴇᴍᴇᴍʙᴇʀ ɪᴛ ɴᴇxᴛ ᴛɪᴍᴇ.**")
                DICT.pop(chat_id)
            except errors.FloodWait as e:
                await asyncio.sleep(e.value)



# ==================================================================== #

@Hiroko.on_message(filters.command("grab", prefixes="/"))
async def grab_waifus(client, message):
    chat_id = message.chat.id
    if chat_id not in DICT or not DICT[chat_id]['name']:
        return await message.reply("No character to grab at the moment. Keep an eye out for the next one!")
    user_id = message.from_user.id
    if len(message.text) < 6:
        return await message.reply("Usage:- `/grab waifu name`")
    guess = message.text.split(maxsplit=1)[1].lower()
    name = DICT[chat_id]['name'].lower()
    wname = DICT[chat_id]['name']
    if guess == name:
        user_id = str(message.from_user.id)
        cusr.execute(
            "INSERT INTO grabbed (user_id, photo , name , anime , rarity) VALUES (%s, %s, %s, %s, %s)",
            (user_id, DICT[chat_id]['photo'], DICT[chat_id]['name'], DICT[chat_id]['anime'], DICT[chat_id]['rarity'])
        )
        DB.commit()
        DICT.pop(chat_id)
        await message.reply(f"**ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ**| {message.from_user.mention} 🎉\n**ʏᴏᴜ ʜᴀᴠᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏʟʟᴇᴄᴛᴇᴅ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ**\n**ɴᴀᴍᴇ**: <code>{wname}</code>")
    else:
        await message.reply("❌ Rip, that's not quite right.")





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



