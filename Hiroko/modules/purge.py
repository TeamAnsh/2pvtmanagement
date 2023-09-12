import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from Hiroko import Hiroko
from config import COMMAND_HANDLER
from Hiroko.Helper.cust_p_filters import admin_filter

# ------------------------------------------------------------------------------- #

TG_MAX_SELECT_LEN = 200

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("purge", COMMAND_HANDLER) & admin_filter)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:        
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.id, message.id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                count_del_etion_s += await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                message_ids = []
        if len(message_ids) > 0:
            count_del_etion_s += await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )

    await status_message.edit_text(f"**ᴅᴇʟᴇᴛᴇᴅ {count_del_etion_s} ᴍᴇssᴀɢᴇs**")
    await asyncio.sleep(5)
    await status_message.delete()
    
# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("del")& admin_filter)
async def _del(_, message):
    if message.sender_chat:
        return
    replied = message.reply_to_message
    chat_id = message.chat.id
    if not replied:
        return await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ.**")

    try:
        await Hiroko.delete_messages(chat_id, replied.id)
        await message.delete()
    except:
        pass


# ------------------------------------------------------------------------------- #



        
