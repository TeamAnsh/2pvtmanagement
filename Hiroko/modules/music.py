from pyrogram import filters
from Hiroko import Hiroko, userbot
from pyrogram.types import Message


@Hiroko.on_message(command.filters("join"))
async def join_userbot(_,msg:Message):
  chat_id = message.chat.id
  invitelink = await Hiroko.export_chat_invite_link(chat_id)
  await userbot.join_chat(invitelink)
  await msg.reply("assistant successfully join.")



downloads = os.path.realpath("downloads")

@Hiroko.on_message(filters.command(["rmd", "clear"], prefixes=["/", "!"]))
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("✅ **ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇs**")
    else:
        await message.reply_text("❌ **ɴᴏ ғɪʟᴇs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ**")



