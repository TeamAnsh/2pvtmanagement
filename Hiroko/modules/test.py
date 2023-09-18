from gtts import gTTS
import os
from Hiroko import Hiroko, pytgcalls
from pyrogram import filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from io import BytesIO



# Function to convert text to audio
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file_path = 'output.mp3'
    tts.save(audio_file_path)
    return audio_file_path

# Function to play audio in a voice chat
async def play_audio_in_voice_chat(chat_id, audio_file_path):
    with open(audio_file_path, "rb") as f:
        audio_data = f.read()
    
    input_audio_stream = InputStream(
        BytesIO(audio_data)
    )

    await pytgcalls.join_group_call(
        chat_id,
        InputAudioStream,
        stream_type=StreamType().local_stream,
    )

# Define a command handler for /audio
@Hiroko.on_message(filters.command("audio", prefixes="/"))
async def audio_command(client, message):
    try:
        chat_id = message.chat.id
        text = message.text.split(None, 1)[1]
        
        # Convert the text to audio
        audio_file_path = text_to_audio(text)
        
        # Play the audio in the voice chat
        await play_audio_in_voice_chat(chat_id, audio_file_path)
    except IndexError:
        await message.reply_text("Please provide text to convert to audio using /audio.")



