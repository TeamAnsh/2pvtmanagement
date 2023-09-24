from asyncio import sleep
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message
from Hiroko.Helper.cust_p_filters import admin_filter
from Hiroko import Hiroko



@Hiroko.on_message(filters.command("purge") & admin_filter)
async def purge(hiroko: Hiroko, msg: Message):

    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="Cannot purge messages in a basic group")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await hiroko.delete_messages(
                    chat_id=msg.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await msg.delete()
        except MessageDeleteForbidden:
            await msg.reply_text(
                text="Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup."
            )
            return
        except RPCError as ef:
            await msg.reply_text(
                text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
            )

        count_del_msg = len(message_ids)

        sumit = await msg.reply_text(text=f"Deleted <i>{count_del_msg}</i> messages")
        await sleep(3)
        await sumit.delete()
        return
    await msg.reply_text("Reply to a message to start purge !")
    return


@Hiroko.on_message(filters.command("spurge") & admin_filter)
async def spurge(c: Hiroko, m: Message):

    if m.chat.type != ChatType.SUPERGROUP:
        await m.reply_text(text="Cannot purge messages in a basic group")
        return

    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.id, m.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(
                text="Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup."
            )
            return
        except RPCError as ef:
            await m.reply_text(
                text=f"""Some error occured, report it using `/bug`

      <b>Error:</b> <code>{ef}</code>"""
            )
        return
    await m.reply_text("Reply to a message to start spurge !")
    return


@Hiroko.on_message(filters.command("del") & admin_filter)
async def del_msg(c: Hiroko, m: Message):

    if m.chat.type != ChatType.SUPERGROUP:
        return

    if m.reply_to_message:
        await m.delete()
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.reply_to_message.id,
        )
    else:
        await m.reply_text(text="What do you wanna delete?")
    return


