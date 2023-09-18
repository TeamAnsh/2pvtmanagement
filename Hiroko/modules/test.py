from gtts import gTTS
import os
from Hiroko import Hiroko, pytgcalls
from pyrogram import filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from io import BytesIO



active_calls = {}

def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    file_path = 'output.mp3'
    tts.save(file_path)
    return file_path



@Hiroko.on_message(filters.command("audio", prefixes="/"))
async def audio_command(client, message):
    try:
        if message.chat.id not in active_calls:
            text = message.text.split(None, 1)[1]
            file_path = text_to_audio(text)
            with open(file_path, "rb") as f:
                audio_data = f.read()
                await pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        BytesIO(audio_data),
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            
        else:
            await message.reply_text("There is already an active audio stream in this chat.")
    except IndexError:
        await message.reply_text("Please provide text to convert to audio using /audio.")



