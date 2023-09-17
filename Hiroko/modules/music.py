import os, asyncio
from config import OWNER_ID
from pyrogram import filters
from Hiroko import Hiroko, pytgcalls, userbot
from pyrogram.types import Message
from pytgcalls import StreamType
from pyrogram.errors import UserAlreadyParticipant
from pytgcalls.types import StreamAudioEnded
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.exceptions import AlreadyJoinedError



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




@pytgcalls.on_stream_end()
async def on_stream_end(chat_id):
    await pytgcalls.leave_group_call(chat_id)
    



@Hiroko.on_message(filters.command(["play"], prefixes=["/", "!"]))
async def play(_, msg: Message):
    try:
        chat_id = msg.chat.id
        requested_by = msg.from_user.first_name
        invitelink = await Hiroko.export_chat_invite_link(chat_id)
        await userbot.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass

    try:
        audio = msg.reply_to_message.audio or msg.reply_to_message.voice if msg.reply_to_message else None
        if audio:
            sum = await msg.reply_text(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%")   
            file_path = await msg.reply_to_message.download()
            await pytgcalls.join_group_call(chat_id, AudioPiped(file_path), stream_type=StreamType().local_stream)
            os.remove(file_path)
            await sum.delete()   
            await asyncio.sleep(0.1)   
            await msg.reply(f"Now playing song\nRequested by {requested_by}")                        
        else:
            await sum.delete()   
            await asyncio.sleep(0.1)   
            await msg.reply("Please reply to an audio or voice message to play.")
    except AlreadyJoinedError:
        await msg.reply(f"Sorry {msg.from_user.mention}, I'm already playing audio in this chat.")
    except Exception as e:         
        await msg.reply(f"Oops! Something went wrong {e}.")






@Hiroko.on_message(filters.command(["pause"], prefixes=["/", "!"]))    
async def pause(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.pause_stream(chat_id)
        await msg.reply(f"Music player successfully paused\nPaused by {msg.from_user.mention}")
    else:
        await msg.reply(f"Sorry {msg.from_user.mention}, I can't pause because there is no music playing on the voice chat.")


@Hiroko.on_message(filters.command(["resume"], prefixes=["/", "!"]))    
async def resume(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.resume_stream(chat_id)
        await msg.reply(f"Music player successfully resumed\nResumed by {msg.from_user.mention}")
    else:
        await msg.reply(f"Sorry {msg.from_user.mention}, I can't resume because there is no music playing on the voice chat.")


@Hiroko.on_message(filters.command(["end"], prefixes=["/", "!"]))    
async def stop(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.leave_group_call(chat_id)
        await msg.reply(f"Music player successfully ended\nEnded by {msg.from_user.mention}")
    else:
        await msg.reply(f"Sorry {msg.from_user.mention}, I can't end music because there is no music playing on the voice chat.")

@Hiroko.on_message(filters.command(["leavevc"], prefixes=["/", "!"]))    
async def leavevc(_, msg: Message):
    chat_id = msg.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await msg.reply(f"Music player successfully leave\nleaved by {msg.from_user.mention}")
    
@Hiroko.on_message(filters.command("volume"))
async def volume(_,msg):
       chat_id = msg.chat.id
       await pytgcalls.change_volume_call(chat_id, 60)
       await msg.reply("volume 60 percent set")


@Hiroko.on_message(filters.command("ume", prefixes="/"))
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"Volume set to {volume}%")
    else:
        await message.reply("Usage: /volume [0-100]")




