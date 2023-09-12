import logging
import time
import asyncio
import datetime
from Hiroko import Hiroko
from config import OWNER_ID
from Hiroko.Helper.database.chatsdb import *
from Hiroko.Helper.database.usersdb import *
from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, ChatAdminRequired


# Broadcast messages to individual users

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


# Broadcast messages to all users

@Hiroko.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def broadcast_to_all(bot, message):
    users = await get_served_users()
    b_msg = message.reply_to_message
    status = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0
    
    for user in users:
        success, reason = await broadcast_messages(int(user['user_id']), b_msg)
        if success:
            success += 1
        elif success is False:
            if reason == "Blocked":
                blocked += 1
            elif reason == "Deleted":
                deleted += 1
            elif reason == "Error":
                failed += 1
        done += 1
        
        if not done % 20:
            await status.edit(f"Broadcast in progress:\n\nTotal Users: {len(users)}\nCompleted: {done}/{len(users)}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await status.edit(f"Broadcast completed:\n\nTotal Users: {len(users)}\nCompleted: {done}/{len(users)}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}\n\nTime taken: {time_taken}")


# Broadcast messages to all groups

@Hiroko.on_message(filters.command("groupcast") & filters.user(OWNER_ID) & filters.reply)
async def group_cast(bot, message):
    chats = await get_served_chats()
    b_msg = message.reply_to_message
    status = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    done = 0
    failed = 0
    success = 0
    
    for chat in chats:
        success, reason = await broadcast_messages(int(chat['chat_id']), b_msg)
        if success:
            success += 1
        elif success is False:
            if reason == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await status.edit(f"Broadcast in progress:\n\nTotal Chats: {len(chats)}\nCompleted: {done}/{len(chats)}\nSuccess: {success}\nFailed: {failed}")
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await status.edit(f"Broadcast completed:\n\nTotal Chats: {len(chats)}\nCompleted: {done}/{len(chats)}\nSuccess: {success}\nFailed: {failed}\n\nTime taken: {time_taken}")

