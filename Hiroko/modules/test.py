import os
import time
from pyrogram import Client, filters
import openai
from config import MONGO_URL
from gtts import gTTS
from pyrogram.types import *
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from Hiroko import Hiroko
from pyrogram.enums import ChatAction, ChatMemberStatus, ParseMode, ChatType
    



mongo = MongoCli(MONGO_URL)
db = mongo["chatgpt_db"]
collection = db["chatgpt_settings"]


openai.api_key = "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"




async def process_question_text(hiroko :Hiroko, question, chat_id):
    MODEL = "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0.2)
    response_text = resp['choices'][0]["message"]["content"]
    await hiroko.send_message(chat_id, response_text)


async def process_question_audio(hiroko :Hiroko, question, chat_id):
    MODEL = "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0.2)
    response_text = resp['choices'][0]["message"]["content"]
    
    tts = gTTS(text=response_text, lang='en')
    audio_file_name = "Hiroko.mp3"
    tts.save(audio_file_name)
        
    await hiroko.send_audio(chat_id, audio=audio_file_name, caption="Here's your voice answer message!")    
    os.remove(audio_file_name)


def get_chat_mode(chat_id):
    chat_mode = collection.find_one({"chat_id": chat_id})
    if chat_mode:
        return chat_mode.get("mode", "text")
    else:
        return "unset"


def set_chat_mode(chat_id, mode):
    collection.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)






@Hirko.on_message(filters.command(["gptmode"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def gpt_mode(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = await Hiroko.get_chat_member(chat_id, user_id)
    
    if message.chat.type == ChatType.Private:
        return await message.reply("This command can only be used in group chats.")
    
    if is_admin.status == ChatMemberStatus.ADMINISTRATOR or is_admin.status == ChatMemberStatus.OWNER:
        await message.reply_text("Please select a mode first:", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Audio Mode", callback_data="mode_audio"),
                    InlineKeyboardButton("Text Mode", callback_data="mode_text"),
                ]
            ]
        ))
    else:
        await message.reply_text("Only group admins can set the mode.")






    
@Hiroko.on_callback_query(filters.regex("mode_audio"))
async def set_mode_callback(hiroko :Hiroko, query):
    chat_id = query.message.chat.id
    user_id = query.from_user.id    
    is_admin = await hiroko.get_chat_member(chat_id, user_id)
    
    if is_admin.status == ChatMemberStatus.ADMINISTRATOR or is_admin.status == ChatMemberStatus.OWNER:
        set_chat_mode(chat_id, "audio")  # Fixed: Pass "audio" as a string
        return await query.answer("Chat mode set to: audio mode")   
        
    await query.answer("Only group admins can change the mode.")

@Hiroko.on_callback_query(filters.regex("mode_text"))
async def set_mode_callback(hiroko :Hiroko, query):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    is_admin = await hiroko.get_chat_member(chat_id, user_id)
    
    if is_admin.status == ChatMemberStatus.ADMINISTRATOR or is_admin.status == ChatMemberStatus.OWNER:
        set_chat_mode(chat_id, "text")  # Fixed: Pass "text" as a string
        return await query.answer("Chat mode set to: text mode")   
        
    await query.answer("Only group admins can change the mode.")




@Hiroko.on_message(filters.command(["assis"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat(hiroko :Hiroko, message):
    chat_id = message.chat.id
    chat_mode = get_chat_mode(chat_id)
    
    if chat_mode == "unset":
        await message.reply_text("Please choose a mode first using /gptmode")
        return

    try:
        await hiroko.send_chat_action(chat_id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text("Hello! Please provide a question like this: /assistant How to set up a database?")
        else:
            question = message.text.split(' ', 1)[1]
            if chat_mode == "audio":
                
                await process_question_audio(hiroko, question, chat_id)
            else:
                
                await process_question_text(hiroko, question, chat_id)

    except Exception as e:
        await message.reply_text(f"Error: {e}")




                                   
