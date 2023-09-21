import os
import time
from pyrogram import Client, filters
import openai
from gtts import gTTS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo

# Initialize MongoDB client
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["chatgpt_db"]
collection = db["chatgpt_settings"]

openai.api_key = "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"

@Hiroko.on_message(filters.command(["setmode"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def set_mode(hiroko, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    is_admin = await hiroko.get_chat_member(chat_id, user_id)
    
    if not is_admin or is_admin.status not in ("creator", "administrator"):
        await message.reply_text("Only group admins can change the mode.")
        return

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Audio Mode", callback_data="mode_audio"),
                InlineKeyboardButton("Text Mode", callback_data="mode_text"),
            ]
        ]
    )

    await message.reply_text("Please select a mode:", reply_markup=buttons)


@Hiroko.on_callback_query(filters.regex("^mode_"))
async def set_mode_callback(hiroko, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    mode = callback_query.data.split("_")[1]

    is_admin = await hiroko.get_chat_member(chat_id, user_id)
    
    if not is_admin or is_admin.status not in ("creator", "administrator"):
        await callback_query.answer("Only group admins can change the mode.")
        return

    set_chat_mode(chat_id, mode)
    await callback_query.answer(f"Chat mode set to: {mode}")

@Hiroko.on_message(filters.command(["assistant"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat(hiroko, message):
    try:
        chat_id = message.chat.id
        chat_mode = get_chat_mode(chat_id)
        await hiroko.send_chat_action(chat_id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text("Hello! Please provide a question like this: /assistant How to set up a database?")
        else:
            question = message.text.split(' ', 1)[1]
            if chat_mode == "audio":
                # Process the question and send an audio response
                await process_question_audio(hiroko, question, chat_id)
            else:
                # Process the question and send a text response
                await process_question_text(hiroko, question, chat_id)

    except Exception as e:
        await message.reply_text(f"Error: {e}")



