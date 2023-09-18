
import os, aiofiles, aiohttp, ffmpeg, random, textwrap, re
import numpy as np
import requests
from os import path
from Hiroko import Hiroko, pytgcalls, userbot
from typing import Callable
from pyrogram import filters, Client
from pyrogram.types import *
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty
from PIL import ImageGrab
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from pyrogram.errors import UserAlreadyParticipant
from Hiroko.Helper.requirements import queues, converter, downloader, DurationLimitError, get_url, get_file_name            
from Hiroko.Helper.admins import admins as a, set
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped


DURATION_LIMIT = float(300)

keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("50%", callback_data="volume_50"),
            InlineKeyboardButton("100%", callback_data="volume_100"),
        ],
        [      
            InlineKeyboardButton("150%", callback_data="volume_150"),
            InlineKeyboardButton("200%", callback_data="volume_200")   
        ]
    ])





que = {}

chat_id = None
useer = "NaN"


def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)



def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 27:        
            text1 += " " + i
        elif len(text2) + len(i) < 25:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]



def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image = Image.open(f"./background.png")
    black = Image.open("Hiroko/Helper/resources/black.jpg")
    img = Image.open("Hiroko/Helper/resources/music.png")
    image5 = changeImageSize(1280, 720, img)
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(10))
    image11 = changeImageSize(1280, 720, image)
    image1 = image11.filter(ImageFilter.BoxBlur(20))
    image1 = image11.filter(ImageFilter.BoxBlur(20))
    image2 = Image.blend(image1,black,0.6)

    im = image5
    im = im.convert('RGBA')
    color = make_col()

    data = np.array(im)
    red, green, blue, alpha = data.T

    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = color

    im2 = Image.fromarray(data)
    image5 = im2


    image3 = image11.crop((280,0,1000,720))
    lum_img = Image.new('L', [720,720] , 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
    img_arr =np.array(image3)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    image3 = Image.fromarray(final_img_arr)
    image3 = image3.resize((600,600))
    
    image2.paste(image3, (50,70), mask = image3)
    image2.paste(image5, (0,0), mask = image5)

    
    font1 = ImageFont.truetype(r'Hiroko/Helper/resources/robot.otf', 30)
    font2 = ImageFont.truetype(r'Hiroko/Helper/resources/robot.otf', 60)
    font3 = ImageFont.truetype(r'Hiroko/Helper/resources/robot.otf', 49)
    font4 = ImageFont.truetype(r'Hiroko/Helper/resources/hiroko.ttf', 35)

    image4 = ImageDraw.Draw(image2)
    image4.text((10, 10), "HIROKO MUSIC", fill="white", font = font1, align ="left") 
    image4.text((670, 150), "NOW PLAYING", fill="white", font = font2, stroke_width=2, stroke_fill="white", align ="left") 

    
    title1 = truncate(title)
    image4.text((670, 280), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((670, 332), text=title1[1], fill="white", font = font3, align ="left") 

    
    views = f"Views : {views}"
    duration = f"Duration : {duration} minutes"
    channel = f"Channel : T-Series"


    
    image4.text((670, 410), text=views, fill="white", font = font4, align ="left") 
    image4.text((670, 460), text=duration, fill="white", font = font4, align ="left") 
    image4.text((670, 510), text=channel, fill="white", font = font4, align ="left")

    
    image2.save(f"final.png")
    os.remove(f"background.png")
    final = f"temp.png"
    return final


@Hiroko.on_message(filters.command(["yt", "play"], prefixes=["/", "!"]))    
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**")
   
    bsdk = message.from_user.mention    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**» sᴏɴɢ ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇ's ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/00411492c1fb4c0a91f18.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )


""""
import os, asyncio, re
from config import OWNER_ID
from pyrogram import filters
from Hiroko import Hiroko, pytgcalls, userbot
from pyrogram.types import *
from pytgcalls import StreamType
from pyrogram.errors import UserAlreadyParticipant
from pytgcalls.types import StreamAudioEnded
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.exceptions import AlreadyJoinedError



keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("50%", callback_data="volume_50"),
            InlineKeyboardButton("100%", callback_data="volume_100"),
        ],
        [      
            InlineKeyboardButton("150%", callback_data="volume_150"),
            InlineKeyboardButton("200%", callback_data="volume_200")   
        ]
    ])

"""

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
    


"""
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
            await msg.reply(f"Now playing song\nRequested by {requested_by}", reply_markup=keyboard)                        
        else:               
            await msg.reply("Please reply to an audio or voice message to play.")
            await sum.delete()       
    except AlreadyJoinedError:
        await msg.reply(f"Sorry {msg.from_user.mention}, I'm already playing audio in this chat.")
    except Exception as e:         
        await msg.reply(f"Oops! Something went wrong {e}.")

"""




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
    await msg.reply(f"Music player successfully leave\nleaved by {msg.from_user.mention}",)
    

@Hiroko.on_message(filters.command("volume", prefixes="/"))
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"Volume set to {volume}%")
    else:
        await message.reply("Usage: /volume [0-100]")



volume_regex = re.compile(r'^volume_(50|100|150|200)$')

@Hiroko.on_callback_query(volume_regex)
async def handle_volume_callback(client, query):
    chat_id = query.message.chat.id
    volume = int(query.data.split("_")[1])
    await pytgcalls.change_volume_call(chat_id, volume)
    await query.answer(f"Volume set to {volume}%")



