from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters, Client
from Hiroko import Hiroko
from config import OWNER_ID
from pyrogram.types import Message
from config import COMMAND_HANDLER
from Hiroko.Helper.cust_p_filters import admin_filter
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)





# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("pin", COMMAND_HANDLER) & admin_filter)
def pin(_, message):
      chat = message.chat
      chat_title = message.chat.title
      chat_id = message.chat.id
      user_id = message.from_user.id
      first_name = message.from_user.first_name
      
      if message.chat.type == enums.ChatType.PRIVATE:
            return message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    
      user_stats = Hiroko.get_chat_member(chat_id, user_id)
      if user_stats.privileges.can_pin_messages and not message.reply_to_message:
         
          try:
            message_id = int(message.text.split(None,1)[1])
            bot.pin_chat_message(chat_id, message_id)
            message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {message.chat.title}\n**ᴀᴅᴍɪɴ:** {first_name}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ",url=f"t.me/{message.chat.username}/{message.id}")]]))
          except Exception as e:
                 return message.reply_text(str(e))

      else:
          try:
            if user_stats.privileges.can_pin_messages and message.reply_to_message:
               message.reply_to_message.pin()
               message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {message.chat.title}\n**ᴀᴅᴍɪɴ:** {first_name}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ",url=f"t.me/{message.chat.username}/{message.id}")]]))
          except Exception as e:
                return message.reply_text(str(e))



# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("unpin", COMMAND_HANDLER) & admin_filter)
def unpin(_, message):
      chat = message.chat
      chat_title = message.chat.title
      chat_id = message.chat.id
      user_id = message.from_user.id
      first_name = message.from_user.first_name
      
      if message.chat.type == enums.ChatType.PRIVATE:
            return message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    
      user_stats = Hiroko.get_chat_member(chat_id, user_id)
      if user_stats.privileges.can_pin_messages and not message.reply_to_message:
         
          try:
            message_id = int(message.text.split(None,1)[1])    
            bot.unpin_chat_message(chat_id, message_id)
            message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {message.chat.title}\n**ᴀᴅᴍɪɴ:** {first_name}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ",url=f"t.me/{message.chat.username}/{message.id}")]]))
          except Exception as e:
                 return message.reply_text(str(e))

      else:
          try:
            if user_stats.privileges.can_pin_messages and message.reply_to_message:
               message.reply_to_message.unpin()
               message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {message.chat.title}\n**ᴀᴅᴍɪɴ:** {first_name}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ",url=f"t.me/{message.chat.username}/{message.id}")]]))
          except Exception as e:
                return message.reply_text(str(e))


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("removephoto", COMMAND_HANDLER)& admin_filter)
async def deletechatphoto(_, message):
      
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ....")
      admin_check = await Hiroko.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`") 
      try:
         if admin_check.privileges.can_change_info:
             await Hiroko.delete_chat_photo(chat_id)
             await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ғʀᴏᴍ ɢʀᴏᴜᴘ !\nʙʏ** {}".format(message.from_user.mention))    
      except:
          await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʀᴇᴍᴏᴠᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("setphoto", COMMAND_HANDLER)& admin_filter)
async def setchatphoto(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
      admin_check = await Hiroko.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`") 
      elif not reply:
           await msg.edit("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.**")
      elif reply:
          try:
             if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
             else:
                await msg.edit("`sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴘʜᴏᴛᴏ !`")
     
          except:
              await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("settitle", COMMAND_HANDLER)& admin_filter)
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    if message.chat.type == enums.ChatType.PRIVATE:
          await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**")
    elif reply:
          try:
            title = message.reply_to_message.text
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
          except AttributeError:
                await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")   
    elif len(message.command) >1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
        except AttributeError:
               await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")
          

    else:
       await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ **")


# --------------------------------------------------------------------------------- #



@Hiroko.on_message(filters.command("setdiscription", COMMAND_HANDLER) & admin_filter)
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ɪɴsᴇʀᴛ!\nʙʏ {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!")   
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ɪɴsᴇʀᴛ!\nʙʏ {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!")
    else:
        await msg.edit("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛᴏɴ!")


# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("leave", COMMAND_HANDLER)& filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    text = "**sᴜᴄᴄᴇssғᴜʟʟʏ ʜɪʀᴏᴋᴏ ʀᴏʙᴏᴛ ʟᴇғᴛ ᴛʜᴇ ɢʀᴏᴜᴘ !!.**"
    await message.reply_text(text)
    await Hiroko.leave_chat(chat_id=chat_id, delete=True)


# --------------------------------------------------------------------------------- #


