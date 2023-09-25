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

    response = f"**ʜᴇʟʟᴏ** {message.from_user.mention} **ʜᴇʀᴇ ʏᴏᴜʀ ᴡᴀɪꜰᴜꜱ**\n"
    for waifu in waifus:
        name, anime, rarity = waifu
        response += f"⊱ {anime}\n⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n⊚ **ᴡᴀɪғᴜ** : {name}\n⊚ **ʀᴀʀɪᴛʏ** |{random.choice(rarity_colour)}| {rarity}\n⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n"

    await message.reply(response)


# ғɪx.ᴋʀɴᴀ. ʜᴀɪ.ʏʜᴀ sᴇ 

@Hiroko.on_message(filters.command("giftwaifu", prefixes="/"))
async def gift_waifu(client, message):
    if len(message.text.split()) != 3:
        await message.reply("Usage: `/giftwaifu @recipient_username waifu_name`")
        return

    recipient_username = message.text.split()[1]
    waifu_name = message.text.split()[2]
    sender_user_id = str(message.from_user.id)

    # Check if the sender has the waifu in their collection
    cusr.execute("SELECT user_id, rarity FROM grabbed WHERE user_id=%s AND name=%s", (sender_user_id, waifu_name))
    sender_waifu = cusr.fetchone()

    if not sender_waifu:
        await message.reply(f"You don't have the waifu '{waifu_name}' in your collection.")
        return

    # Check if the recipient exists and get their user_id
    recipient = await client.get_users(recipient_username)
    if not recipient:
        await message.reply(f"User '{recipient_username}' not found.")
        return
    recipient_user_id = str(recipient.id)

    # Transfer the waifu to the recipient
    try:
        cusr.execute(
            "UPDATE grabbed SET user_id=%s WHERE user_id=%s AND name=%s",
            (recipient_user_id, sender_user_id, waifu_name)
        )
        DB.commit()
    except Exception as e:
        print(f"Error transferring waifu: {e}")
        await message.reply("An error occurred while transferring the waifu.")
        return

    await message.reply(f"Successfully gifted '{waifu_name}' to {recipient_username}.")


    
    


@Hiroko.on_message(filters.command("topwaifugrabbers", prefixes="/"))
async def top_waifu_grabs(client, message):
    try:
        # Fetch the top 10 waifu collectors
        cusr.execute("SELECT user_id, COUNT(*) as waifu_count FROM grabbed GROUP BY user_id ORDER BY waifu_count DESC LIMIT 10")
        top_collectors = cusr.fetchall()

        if not top_collectors:
            await message.reply("No waifu collectors found.")
            return

        # Extract user_ids and waifu counts
        user_ids = [str(collector[0]) for collector in top_collectors]
        waifu_counts = [collector[1] for collector in top_collectors]

        # Get usernames for display
        usernames = []
        for user_id in user_ids:
            user = await client.get_users(int(user_id))
            usernames.append(user.username if user.username else f"User {user_id}")

        # Create a bar graph to display waifu counts
        plt.figure(figsize=(10, 6))
        plt.barh(usernames, waifu_counts, color='red')
        plt.xlabel('Waifu Count')
        plt.ylabel('User')
        plt.title('Top 10 Waifu Collectors')
        plt.gca().invert_yaxis()

        # Save the graph as an image
        graph_filename = 'top_waifu_collectors.png'
        plt.savefig(graph_filename, bbox_inches='tight', format='png')
        plt.close()

        # Send the graph as a photo
        await message.reply_photo(photo=graph_filename, caption="Top 10 Waifu Collectors")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("An error occurred while fetching top collectors.")








@Hiroko.on_message(filters.command("topwaifugroups", prefixes="/"))
async def top_waifu_groups(client, message):
    try:
        # Fetch the top 5 waifu collector groups
        cusr.execute("SELECT chat_id, COUNT(*) as waifu_count FROM grabbed GROUP BY chat_id ORDER BY waifu_count DESC LIMIT 5")
        top_groups = cusr.fetchall()

        if not top_groups:
            await message.reply("No waifu collector groups found.")
            return

        # Extract chat_ids and waifu counts
        chat_ids = [str(group[0]) for group in top_groups]
        waifu_counts = [group[1] for group in top_groups]

        # Get group names for display
        group_names = []
        for chat_id in chat_ids:
            chat_info = await client.get_chat(chat_id)
            group_names.append(chat_info.title)

        # Create a 3D pie chart to display group percentages
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.pie(waifu_counts, labels=group_names, autopct='%1.1f%%', startangle=90)

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Top 5 Waifu Collector Groups')

        # Save the graph as an image
        graph_filename = 'top_waifu_groups.png'
        plt.savefig(graph_filename, bbox_inches='tight', format='png')
        plt.close()

        # Send the graph as a photo
        await message.reply_photo(photo=graph_filename, caption="Top 5 Waifu Collector Groups")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("An error occurred while fetching top groups.")





