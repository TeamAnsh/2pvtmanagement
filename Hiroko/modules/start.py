import logging
import asyncio
import random
import time
import datetime 
from config import BOT_USERNAME, OWNER_ID
from pyrogram import filters, Client
from Hiroko import Hiroko
from pyrogram.enums import ChatType 
from pyrogram.errors import MessageNotModified, InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, ChatAdminRequired
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko.Helper.database.chatsdb import * 
from Hiroko.Helper.database.usersdb import *
from Hiroko.modules.text import SHORTENER_TEXT, ADMINS_TEXT, GITHUB_TEXT, FUN_TEXT, MISC_TEXT, NEKOS_TEXT, GAMES_TEXT, CHATGPT_TEXT, CHATBOT_TEXT, INSTATUS_TEXT, AFK_TEXT, ACTION_TEXT         



# ------------------------------------------------------------------------------- #

START_IMG = (
"https://graph.org/file/f035f0e34969c14ae2e8c.jpg",
"https://graph.org/file/68227791cf9273fbede7a.jpg",
"https://graph.org/file/d91ec80b019d43082965d.jpg",
"https://graph.org/file/d6ae49af114fa50d5ba89.jpg",
"https://graph.org/file/30f6cc0b6251afe5c4153.jpg",
"https://telegra.ph/file/0214edaebad6ef6d69c1d.jpg",
"https://telegra.ph/file/f658925a255bea26efaa4.jpg",
"https://telegra.ph/file/235e4c7e9dd0c48bac638.jpg",

)



# ------------------------------------------------------------------------------- #

START_TEXT = """
**ʜᴇʏ ᴛʜᴇʀᴇ [{}](tg://user?id={}) ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**
━━━━━━━━━━━━━━━━━━━━━━**
๏ ɪ ᴀᴍ ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs
๏ ɪ ᴀᴍ ᴅɪғғᴇʀᴇɴᴛ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛs

๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs**
"""


# ------------------------------------------------------------------------------- #

HELP_TEXT = """**
» ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴄᴏᴏʟ ᴏʀ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs 

» ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ / ᴏʀ !
» ɪꜰ ʏᴏᴜ ɢᴏᴛ ᴀɴʏ ɪssᴜᴇ ᴏʀ ʙᴜɢ ɪɴ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅ ᴘʟᴇᴀsᴇ ʀᴇᴘᴏʀᴛ ɪᴛ ᴀᴛ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](https://t.me/TheNixaSupport)**
ㅤㅤㅤㅤㅤㅤ
‣<code> /start</code> : **ꜱᴛᴀʀᴛꜱ ᴍᴇ | ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴᴇ ɪᴛ.**
‣<code> /donate</code> : **sᴜᴘᴘᴏʀᴛ ᴍᴇ ʙʏ ᴅᴏɴᴀᴛɪɴɢ ꜰᴏʀ ᴍʏ ʜᴀʀᴅᴡᴏʀᴋ.**
"""



# ------------------------------------------------------------------------------- #

hiroko_buttons = [              
                [
                    InlineKeyboardButton("ᴀғᴋ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴀᴅᴍɪɴs", callback_data="admins_"),
                    InlineKeyboardButton("ғᴜɴ", callback_data="fun_")
                ],
                [
                    InlineKeyboardButton("ɢɪᴛʜᴜʙ", callback_data="github_"),   
                    InlineKeyboardButton("ɪɴsᴛᴀᴛᴜs", callback_data="instatus_"),
                    InlineKeyboardButton("ɴᴇᴋᴏs", callback_data="nekos_")
                ],
                [
                    InlineKeyboardButton("ᴄʜᴀᴛʙᴏᴛ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴍɪsᴄ", callback_data="misc_"),
                    InlineKeyboardButton("sʜᴏʀᴛᴇɴᴇʀ", callback_data="shortener_")
                ],
                [
                    InlineKeyboardButton("ɢᴀᴍᴇs", callback_data="action_"),   
                    InlineKeyboardButton("ᴄʜᴀᴛɢᴘᴛ", callback_data="chatgpt_"),
                    InlineKeyboardButton("ᴀᴄᴛɪᴏɴ", callback_data="action_")
                ],             
                [
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),
                    InlineKeyboardButton("⟲ ᴄʟᴏꜱᴇ ⟳", callback_data="close_data")
                ]
                ]


back_buttons  = [[
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="help_"),                    
                ]]

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client: Client, message: Message):    
        get_me = await client.get_me()
        BOT_USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/TheNixaSupport"),
                InlineKeyboardButton("🎓 ᴍᴀɪɴᴛᴀɪɴᴇʀ", url=f"https://t.me/AnonDeveloper"),
            ],
            [
                InlineKeyboardButton("📚 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 📚", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(START_IMG),
            caption=START_TEXT.format(message.from_user.first_name, message.from_user.id),
            reply_markup=reply_markup
        )
        await add_served_user(message.from_user.id)            
        await add_served_chat(message.chat.id)


# ------------------------------------------------------------------------------- #

@Hiroko.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="home_":
        buttons =  [
            [
                InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/TheNixaSupport"),
                InlineKeyboardButton("🎓 ᴍᴀɪɴᴛᴀɪɴᴇʀ", url=f"https://t.me/AnonDeveloper"),
            ],
            [
                InlineKeyboardButton("📚 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 📚", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                START_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #
        
    elif query.data=="help_":        
        reply_markup = InlineKeyboardMarkup(hiroko_buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

  
# ------------------------------------------------------------------------------- #

    elif query.data=="afk_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                AFK_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

  
# ------------------------------------------------------------------------------- #

    elif query.data=="admins_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                ADMINS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="fun_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                FUN_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass 


# ------------------------------------------------------------------------------- #

    elif query.data=="github_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                GITHUB_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="instatus_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                INSTATUS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="nekos_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                NEKOS_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="chatbot_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                CHATBOT_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="misc_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                MISC_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="shortener_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                SHORTENER_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="games_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                GAMES_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="chatgpt_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                CHATGPT_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="action_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                ACTION_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #

    elif query.data=="maintainer_":
            await query.answer(("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ "), show_alert=True)

  
# ------------------------------------------------------------------------------- #
 
    elif query.data=="close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
          

# ------------------------------------------------------------------------------- #


    elif query.data=="usercast_":      
        users = await get_served_users()
        status = await query.message.reply_text(
            text="**ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs...**"
        )
        start_time = time.time()
        done = 0
        deleted = 0
        success = 0

        for user in users:
            success, reason = await broadcast_messages(int(user['user_id']))
            if success:
                success += 1
            elif success is False:
                if reason == "Deleted":
                    deleted += 1
            done += 1

            if not done % 20:
                await status.edit(f"**ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss**:\n\**nᴛᴏᴛᴀʟ ᴜsᴇʀs**: {len(users)}\n**ᴄᴏᴍᴘʟᴇᴛᴇᴅ**: {done}/{len(users)}\n**ᴅᴇʟᴇᴛᴇᴅ**: {deleted}")

        time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
        await status.edit(f"**ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**:\n\n**ᴛᴏᴛᴀʟ ᴜsᴇʀs**: {len(users)}\n**ᴄᴏᴍᴘʟᴇᴅᴛᴇᴅ**: {done}/{len(users)}\n**ᴅᴇʟᴇᴛᴇᴅ**: {deleted}\n\n**ᴛɪᴍᴇ ᴛᴀᴋᴇɴ**: {time_taken}")



# ------------------------------------------------------------------------------- #

  
    elif query.data=="groupcast_":
        chats = await get_served_chats()
        status = await query.message.reply_text(
            text="**ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs...**"
        )
        start_time = time.time()
        done = 0
        success = 0

        for chat in chats:
            success, reason = await broadcast_messages(int(chat['chat_id']))
            if success:
                success += 1
            done += 1
            await asyncio.sleep(2)
            if not done % 20:
                await status.edit(f"**ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss**:\n\n**ᴛᴏᴛᴀʟ ᴄʜᴀᴛs**: {len(chats)}\n**ᴄᴏᴍᴘʟᴇᴛᴇᴅ**: {done}/{len(chats)}")

        time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
        await status.edit(f"**ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ**:\n\n**ᴛᴏᴛᴀʟ ᴄʜᴀᴛs**: {len(chats)}\n**ᴄᴏᴍᴘʟᴇᴛᴇᴅ**: {done}/{len(chats)}\n\n**ᴛɪᴍᴇ ᴛᴀᴋᴇɴ**: {time_taken}")



# ------------------------------------------------------------------------------- #


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(int(user_id))
        logging.info(f"{user_id} - Removed from database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} - Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"


# ------------------------------------------------------------------------------- #



