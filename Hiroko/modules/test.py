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
        if len(message.command) < 2:
            await message.reply_text("Please specify a mode: /setmode audio or /setmode text")
        else:
            mode = message.command[1].lower()
            if mode == "audio" or mode == "text":
                set_chat_mode(chat_id, mode)
                await message.reply_text(f"Chat mode set to: {mode}")
            else:
                await message.reply_text("Invalid mode. Please use /setmode audio or /setmode text")

    
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




async def process_question_text(hiroko, question, chat_id):
    MODEL = "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0.2)
    response_text = resp['choices'][0]["message"]["content"]
    await hiroko.send_message(chat_id, response_text)

async def process_question_audio(hiroko, question, chat_id):
    MODEL = "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0.2)
    response_text = resp['choices'][0]["message"]["content"]
    
    # Convert the AI response to audio
    tts = gTTS(text=response_text, lang='en')
    audio_file_name = "assistant_response.mp3"
    tts.save(audio_file_name)
    
    # Send the audio response to the user
    await hiroko.send_audio(chat_id, audio=audio_file_name, caption="Here's your voice answer message!")
    
    # Clean up the temporary audio file
    os.remove(audio_file_name)

def get_chat_mode(chat_id):
    # Retrieve the chat mode from the database, default to "text"
    chat_mode = collection.find_one({"chat_id": chat_id})
    if chat_mode:
        return chat_mode.get("mode", "text")
    else:
        # Default to "text" mode if not found in the database
        return "text"

def set_chat_mode(chat_id, mode):
    # Update the chat mode in the database
    collection.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)



