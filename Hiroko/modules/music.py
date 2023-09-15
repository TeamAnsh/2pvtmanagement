from pyrogram import filters
from Hiroko import Hiroko, userbot
from pyrogram.types import Message


@Hiroko.on_message(command.filters("join"))
async def join_userbot(_,msg:Message):
  chat_id = message.chat.id
  invitelink = await Hiroko.export_chat_invite_link(chat_id)
  await userbot.join_chat(invitelink)
  await msg.reply("assistant successfully join.")

