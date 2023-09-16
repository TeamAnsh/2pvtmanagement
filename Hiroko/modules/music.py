import os
from pyrogram import filters
from Hiroko import Hiroko, pytgcalls, userbot
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped




@Hiroko.on_message(filters.video_chat_started)
async def brah(_, msg):
       await msg.reply("voice chat started")

@Hiroko.on_message(filters.video_chat_ended)
async def brah2(_, msg):
       await msg.reply("voice chat ended")

@Hiroko.on_message(filters.video_chat_members_invited)
async def fuckoff(hiroko :Hiroko, message:Message):
           text = f"{message.from_user.mention} Invited "
           x = 0
           for user in message.video_chat_members_invited.users:
             try:
               text += f"[{user.first_name}](tg://user?id={user.id}) "
               x += 1
             except Exception:
               pass
           try:
             await message.reply(f"{text} 😉")
           except:
             pass


@Hiroko.on_message(filters.command("join"))
async def join_userbot(_,msg:Message):
  chat_id = msg.chat.id
  invitelink = await Hiroko.export_chat_invite_link(chat_id)
  await userbot.join_chat(invitelink)
  await msg.reply("assistant successfully join.")



@Hiroko.on_message(filters.command(["play"], prefixes=["/", "!"]))
async def play(_, msg:Message):
    chat_id = msg.chat.id
    requested_by = msg.from_user.first_name
    audio = (
        msg.reply_to_message.audio or msg.reply_to_message.voice
    ) if msg.reply_to_message else None

    if audio:
           file_path = await msg.reply_to_message.download()
           x = await pytgcalls.join_group_call(
                  chat_id,
                  AudioPiped(
                   file_path,),
                  stream_type=StreamType().local_stream,) 
           os.remove(file_path)
           if x:             
                  await msg.reply(f"now play song \nrequested by {requested_by}")
           await msg.reply("sorry {msg.from_user.mention} wait sir after ending song you can play song.")       
    else:
        await msg.reply("Please reply to an audio or voice message to play.")


    

@Hiroko.on_message(filters.command(["pause"], prefixes=["/", "!"]))    
async def pause(_, msg: Message):
       x = await pytgcalls.pause_stream(msg.chat.id)
       if x:
              await msg.reply("music player successfully paused\n paused by {msg.from_user.mention}")
       await msg.reply("sorry {msg.from_user.mention} i can't paused beacuse does not play any music on voice chat.")
    


@Hiroko.on_message(filters.command(["resume"], prefixes=["/", "!"]))    
async def resume(_, msg: Message):
       x = await pytgcalls.resume_stream(msg.chat.id)
       if x:
              await msg.reply("music player successfully paused\n resumed by {msg.from_user.mention}")
       await msg.reply("sorry {msg.from_user.mention} i can't resume beacuse does not play any music on voice chat.")
    

    
@Hiroko.on_message(filters.command(["end"], prefixes=["/", "!"]))    
async def stop(_, msg: Message):
       x = await pytgcalls.leave_group_call(msg.chat.id)
       if x:
              await msg.reply("music player successfully end\n ended by {msg.from_user.mention}")
       await msg.reply("sorry {msg.from_user.mention} i can't end music beacuse does not play any music on voice chat.")
        



