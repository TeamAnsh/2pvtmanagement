import requests, asyncio, random, psycopg2, json
import matplotlib.pyplot as plt
import numpy as np
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
        return await message.reply("** ʜᴇʟʟᴏ ʜᴏᴛᴛɪᴇ, ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴡᴀɪғᴜ ᴅᴇᴛᴀɪʟs ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ**: /addwaifu photo+name-anime+rarity")
    if not message.text.split(maxsplit=1)[1]:
        return await message.reply("** ʜᴇʟʟᴏ ʜᴏᴛᴛɪᴇ, ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴡᴀɪғᴜ ᴅᴇᴛᴀɪʟs ɪɴ ᴛʜᴇ ғᴏʀᴍᴀᴛ**: /addwaifu photo+name-anime+rarity")
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split("+")
    if not data[0].startswith("https"):
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴡᴀɪғᴜ ʟɪɴᴋ.**")
    if not data[1]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴡᴀɪғᴜ ɴᴀᴍᴇ.**")
    if not data[2]:
        return await message.reply_text("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴀɴɪᴍᴇ ɴᴀᴍᴇ.**")
    if not data[3]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴡᴀɪғᴜ ʀᴀʀɪᴛʏ.**")
    
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
    await Hiroko.send_message(-1001946875647, text=f"**ᴡᴀɪғᴜ ᴜᴘʟᴏᴀᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴇᴄᴋ ᴡᴀɪғᴜs ᴅᴏᴍᴀɪɴ**[🎉]({photo})", reply_markup=InlineKeyboardMarkup([[
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
                await _.send_message(chat_id, f"**ᴀ sᴇxʏ ᴡᴀɪғᴜ ʜᴀꜱ ʀᴀɴ ᴀᴡᴀʏ!!**\n\n**ɴᴀᴍᴇ** : <code>{character}</code>\n**ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ʀᴇᴍᴇᴍʙᴇʀ ɪᴛ ɴᴇxᴛ ᴛɪᴍᴇ.**")
                DICT.pop(chat_id)
            except errors.FloodWait as e:
                await asyncio.sleep(e.value)



# ==================================================================== #

@Hiroko.on_message(filters.command("grab", prefixes="/"))
async def grab_waifus(client, message):
    chat_id = message.chat.id
    if chat_id not in DICT or not DICT[chat_id]['name']:
        return await message.reply("**ɴᴏ sᴇxʏ ᴡᴀɪғᴜ ᴛᴏ ɢʀᴀʙ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ. ᴋᴇᴇᴘ ᴀɴ ᴇʏᴇ ᴏᴜᴛ ғᴏʀ ᴛʜᴇ ɴᴇxᴛ ᴏɴᴇ!**")
    user_id = message.from_user.id
    if len(message.text) < 6:
        return await message.reply("**ʜᴇʏ sᴡᴇᴇᴛʜᴇᴀʀᴛ ᴛʏᴘᴇ ɢʀᴀʙ ᴀɴᴅ ᴡᴀɪғᴜ ɴᴀᴍᴇ ᴜsᴀɢᴇ**:- `/grab waifu name`")
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
        await message.reply(f"**ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ**| {message.from_user.mention} 🎉\n\n**ʏᴏᴜ ʜᴀᴠᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄᴏʟʟᴇᴄᴛᴇᴅ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ**\n**ɴᴀᴍᴇ** : <code>{wname}</code>")
    else:
        await message.reply("❌ **ʀɪᴘ, ᴛʜᴀᴛ's ɴᴏᴛ ǫᴜɪᴛᴇ ʀɪɢʜᴛ.**")





# ==================================================================== #

rarity_colour = [
    "⚫",
    "⚪",
    "🔴",
    "🔵"
]


@Hiroko.on_message(filters.command(["mywaifu","myharem"], prefixes="/"))
async def my_waifus(client, message):
    user_id = str(message.from_user.id)
    
    # Fetch the user's waifus from the database
    cusr.execute("SELECT name, anime, rarity FROM grabbed WHERE user_id=%s", (user_id,))
    waifus = cusr.fetchall()

    if not waifus:
        await message.reply("**ᴀᴡᴡ ʙᴀʙʏ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴄᴏʟʟᴇᴄᴛᴇᴅ ᴀɴʏ ᴡᴀɪғᴜs ʏᴇᴛ.**")
        return

    response = f"**ʜᴇʟʟᴏ** {message.from_user.mention} **ʜᴇʀᴇ ʏᴏᴜʀ ᴡᴀɪꜰᴜꜱ**\n\n"
    for waifu in waifus:
        name, anime, rarity = waifu
        response += f"⊱ {anime}\n⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n⊚ **ᴡᴀɪғᴜ** : {name}\n⊚ **ʀᴀʀɪᴛʏ** |{random.choice(rarity_colour)}| {rarity}\n⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n"

    await message.reply(response)





@Hiroko.on_message(filters.command("giftwaifu", prefixes="/"))
async def gift_waifu(client, message):
    replied = message.reply_to_message
    user_id = message.from_user.id

    if len(message.command) != 3:
        await message.reply("Usage: `/giftwaifu waifu_name` or reply to a user's message with the waifu name.")
        return

    if replied:
        x = message.command[1]
        z = " "
        y = message.command[2]
        
        waifu_name = x + z + y  
        sender_id = str(user_id)
        cusr.execute("SELECT user_id, rarity FROM grabbed WHERE user_id=%s AND name=%s", (sender_id, waifu_name))
        sender_waifu = cusr.fetchone()

        if not sender_waifu:
            await message.reply(f"You don't have the waifu '{waifu_name}' in your collection.")
            return
        recipient_id = str(replied.from_user.id)

        try:
            cusr.execute(
                "UPDATE grabbed SET user_id=%s WHERE user_id=%s AND name=%s",
                (recipient_id, sender_id, waifu_name)
            )
            DB.commit()

            await message.reply(f"Successfully gifted '{waifu_name}' to @{replied.from_user.username}.")
        except Exception as e:
            print(f"Error transferring waifu: {e}")
            await message.reply("An error occurred while transferring the waifu.")
            return
    else:
        await message.reply("Please reply to a user's message with the waifu name you want to gift.")



# =============


current_waifu_photo = None
current_waifu_index = 0

@Hiroko.on_message(filters.command("waifu", prefixes="/"))
async def waifu_command(client, message):
    user_id = message.from_user.id
    sender_id = str(user_id)

    cusr.execute("SELECT name, photo FROM grabbed WHERE user_id=%s", (sender_id,))
    waifus = cusr.fetchall()

    if not waifus:
        await message.reply("You don't have any waifus in your collection.")
        return

    global current_waifu_index
    await send_waifu_message(message.chat.id, user_id, waifus[current_waifu_index])

@Hiroko.on_callback_query(filters.regex(r"^(next_waifu|back_waifu)$"))
async def change_waifu(client, callback_query):
    global current_waifu_index
    data = callback_query.data
    user_id = callback_query.from_user.id  # Get the user_id from the callback_query
    waifus = get_waifus_for_user(user_id)
    if data == "next_waifu":
        current_waifu_index = (current_waifu_index + 1) % len(waifus)
    elif data == "back_waifu":
        current_waifu_index = (current_waifu_index - 1) % len(waifus)
    await send_waifu_message(callback_query.message.chat.id, user_id, waifus[current_waifu_index])
    await callback_query.answer("hehehe")

async def send_waifu_message(chat_id, user_id, waifu):
    global current_waifu_photo
    waifu_name, waifu_photo = waifu
    message_text = f"Current Waifu: {waifu_name}"

    if waifu_photo != current_waifu_photo:
        await Hiroko.send_photo(chat_id, waifu_photo, caption=message_text,
                                reply_markup=get_waifu_buttons())
        current_waifu_photo = waifu_photo
    else:
        await Hiroko.send_message(chat_id, message_text, reply_markup=get_waifu_buttons())

def get_waifu_buttons():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back", callback_data="back_waifu"),
             InlineKeyboardButton("Next", callback_data="next_waifu")],
        ]
    )

def get_waifus_for_user(user_id):
    cusr.execute("SELECT name, photo FROM grabbed WHERE user_id=%s", (str(user_id),))
    return cusr.fetchall()

