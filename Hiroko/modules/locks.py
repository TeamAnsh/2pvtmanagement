from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from Hiroko import Hiroko



@Hiroko.on_message(filters.command("lockall") & filters.group)
def lock_all_chat_permissions(client, message):
    chat_id = message.chat.id
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )
    try:
        client.set_chat_permissions(chat_id, permissions)
        message.reply_text("All chat permissions locked.")
    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")


@Hiroko.on_message(filters.command("unlockall") & filters.group)
def unlock_all_chat_permissions(client, message):
    chat_id = message.chat.id
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_change_info=True,
        can_invite_users=True,
        can_pin_messages=True
    )
    try:
        client.set_chat_permissions(chat_id, permissions)
        message.reply_text("All chat permissions unlocked.")
    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")




