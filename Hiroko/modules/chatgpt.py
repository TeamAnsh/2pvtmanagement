import os
import time
from pyrogram import Client, filters
import openai
from gtts import gTTS
from Hiroko import Hiroko
from pyrogram.enums import ChatAction, ParseMode





openai.api_key = "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"




@Hiroko.on_message(filters.command(["chatgpt","ai","ask"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def chat(hiroko :Hiroko, message):
    
    try:
        start_time = time.time()
        await hiroko.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-**`.ask How to set girlfriend ?`")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            resp = openai.ChatCompletion.create(model=MODEL,messages=[{"role": "user", "content": a}],
    temperature=0.2)
            x=resp['choices'][0]["message"]["content"]
            await message.reply_text(f"{x}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        




@Hiroko.on_message(filters.command(["assistant"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat(hiroko, message):
    try:
        start_time = time.time()
        await hiroko.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            await message.reply_text("Hello! Please provide a question like this: /assistant How to set girlfriend?")
        else:
            question = message.text.split(' ', 1)[1]
            MODEL = "gpt-3.5-turbo"
            
            # Generate AI response
            resp = openai.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": question}], temperature=0.2)
            response_text = resp['choices'][0]["message"]["content"]
            
            # Convert the AI response to audio
            tts = gTTS(text=response_text, lang='en')
            audio_file_name = "assistant_response.mp3"
            tts.save(audio_file_name)
            
            # Send the audio response to the user
            await message.reply_audio(audio=audio_file_name, caption="Here's your voice answer message!")
            
            # Clean up the temporary audio file
            os.remove(audio_file_name)
    
    except Exception as e:
        await message.reply_text(f"Error: {e}")




