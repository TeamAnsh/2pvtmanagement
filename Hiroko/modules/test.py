
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file_path = 'output.mp3'
    tts.save(audio_file_path)
    return audio_file_path

async def play_audio_in_voice_chat(chat_id, audio_file_path):
    input_audio_stream = InputAudioStream(
        file_path=audio_file_path,
    )

    await pytgcalls.join_group_call(
        chat_id,
        InputStream(input_audio_stream),
        stream_type=StreamType().local_stream,
    )



@Hiroko.on_message(filters.command("audio", prefixes="/"))
async def audio_command(client, message):

    audio_file_path = text_to_audio(text)  # Convert the text to audio
    await play_audio_in_voice_chat(message.chat.id, audio_file_path)

