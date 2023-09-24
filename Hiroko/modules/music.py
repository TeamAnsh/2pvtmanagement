import os, aiofiles, aiohttp, ffmpeg, random, textwrap, re
import numpy as np
import requests
from os import path
from Hiroko import Hiroko, pytgcalls, userbot
from typing import Callable
from pyrogram import filters, Client
from pyrogram.types import *
from Hiroko.Helper.cust_p_filters import admin_filter
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty
from PIL import ImageGrab
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from pyrogram.errors import UserAlreadyParticipant
from Hiroko.Helper.requirements import get_url, get_file_name, converter, downloader, admins as a, set_admins as set
from Hiroko.Helper import requirements as rq
from Hiroko.Helper.errors import DurationLimitError
from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream


DURATION_LIMIT = 300

keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("▷", callback_data="music_pause"),
            InlineKeyboardButton("Ⅱ", callback_data="music_resume"),    
            InlineKeyboardButton("Ⓥ", callback_data="music_volume"),      
            InlineKeyboardButton("⊜", callback_data="music_skip"),
            InlineKeyboardButton("⊝", callback_data="music_end"),  
        ],
        [
            InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"),    
        ]
])

button = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("50", callback_data="volume_50"),
            InlineKeyboardButton("100", callback_data="volume_100"),    
            InlineKeyboardButton("150", callback_data="volume_150"),      
            InlineKeyboardButton("1200", callback_data="volume_200"),
                
        ],
        [
            InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"),    
        ]
])


# --------------------------------------------------------------------------------------------------------- #


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

# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["yt", "play"], prefixes=["!"]))
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
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
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
            if not os.path.isfile(os.path.join("downloads", file_name))
            else file_name
        )
            
    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()            
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/00411492c1fb4c0a91f18.jpg"
            duration = "NaN"
            views = "NaN"
            

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter(downloader(url))
    else:
        if len(message.command) < 2:
            await lel.edit(
                     "💌 **ᴜsᴀɢᴇ: /ᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**"
                    
            )
        else:
            await lel.edit("**⇆ ᴘʀᴏᴄᴇssɪɴɢ...**")
        query = message.text.split(None, 1)[1]
        
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"            
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**"
            )
            print(str(e))
            return

        
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter(downloader(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**​🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({url})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{bsdk}",
            reply_markup=keyboard,
        )
       
    else:
        await pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({url})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{bsdk}\n",
           )

    os.remove("final.png")
    return await lel.delete()


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["skip", "next"], prefixes=["/", "!"]) & admin_filter)
async def skip(_, message: Message):    
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if chat_id not in ACTV_CALLS:
        await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴛᴏ sᴋɪᴘ.**")
    else:
        rq.task_done(chat_id)
        if rq.is_empty(chat_id):
            await pytgcalls.leave_group_call(chat_id)
        else:
            await pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        rq.get(chat_id)["file"],
                    ),
                ),
            )
        await message.reply_text("**ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴋɪᴘᴘᴇᴅ ᴛʜᴇ sᴏɴɢ.**")


# --------------------------------------------------------------------------------------------------------- #


@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update) -> None:
    chat_id = update.chat_id
    rq.task_done(chat_id)

    if rq.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        await pytgcalls.change_stream(
            chat_id, 
            InputStream(
                InputAudioStream(
                    rq.get(chat_id)["file"],
                ),
            ),
        )



# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.video_chat_started)
async def brah(_, msg):
       await msg.reply("**ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ**")


# --------------------------------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.video_chat_ended)
async def brah2(_, msg):
       await msg.reply("**ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ**")


# --------------------------------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.video_chat_members_invited)
async def fuckoff(hiroko :Hiroko, message:Message):
           text = f"{message.from_user.mention} ɪɴᴠɪᴛᴇᴅ "
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


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command("join"))
async def join_userbot(_,msg:Message):
  chat_id = msg.chat.id
  invitelink = await Hiroko.export_chat_invite_link(chat_id)
  await userbot.join_chat(invitelink)
  await msg.reply("**ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴ.**")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["pause"], prefixes=["/", "!"]))    
async def pause(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.pause_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴘᴀᴜsᴇᴅ\nᴘᴀᴜsᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴘᴀᴜsᴇᴅ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["resume"], prefixes=["/", "!"]))    
async def resume(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.resume_stream(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴜᴍᴇ\nʀᴇsᴜᴍᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ʀᴇsᴜᴍᴇ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇʀᴇ ɪs ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["end"], prefixes=["/", "!"]))    
async def stop(_, msg: Message):
    chat_id = msg.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.leave_group_call(chat_id)
        await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴅᴇᴅ sᴏɴɢ\nᴇɴᴅᴇᴅ ʙʏ {msg.from_user.mention}")
    else:
        await msg.reply(f"sᴏʀʀʏ {msg.from_user.mention}, ɪ ᴄᴀɴ'ᴛ ᴇɴᴅ ᴍᴜsɪᴄ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["leavevc"], prefixes=["/", "!"]))    
async def leavevc(_, msg: Message):
    chat_id = msg.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await msg.reply(f"ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\nʟᴇᴀᴠᴇᴅ ʙʏ {msg.from_user.mention}",)
    

# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command("volume", prefixes="/"))
async def change_volume(client, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        volume = int(args[1])
        await pytgcalls.change_volume_call(chat_id, volume)
        await message.reply(f"ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ {volume}%")
    else:
        await message.reply("ᴜsᴀɢᴇ: /volume [0-200]")


# --------------------------------------------------------------------------------------------------------- #
#             <--------------------  HERE IS STARTED  RAGEX MUSIC CALLBACK ---------------------->
# --------------------------------------------------------------------------------------------------------- #



@Hiroko.on_callback_query(filters.regex("music_skip"))
async def callback_skip(_, query : CallbackQuery):    
    ACTV_CALLS = []
    chat_id = query.message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if chat_id not in ACTV_CALLS:
        await query.answer("ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴛᴏ sᴋɪᴘ.")
    else:
        rq.task_done(chat_id)
        if rq.is_empty(chat_id):
            await pytgcalls.leave_group_call(chat_id)
        else:
            await pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        rq.get(chat_id)["file"],
                    ),
                ),
            )
        await query.answer("ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴋɪᴘᴘᴇᴅ ᴛʜᴇ sᴏɴɢ.")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_callback_query(filters.regex("music_pause"))
async def callback_pause(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.pause_stream(chat_id)
        await query.answer("ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴘᴀᴜsᴇᴅ.")
    else:
        await query.answer("sᴏʀʀʏ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")

# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_callback_query(filters.regex("music_resume"))
async def callback_resume(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.resume_stream(chat_id)
        await query.answer("ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇsᴜᴍᴇᴅ.")
    else:
        await query.answer("sᴏʀʀʏ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_callback_query(filters.regex("music_end"))
async def callback_end(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    if str(chat_id) in str(pytgcalls.active_calls):
        await pytgcalls.leave_group_call(chat_id)
        await query.answer("ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴅᴇᴅ sᴏɴɢ.")
    else:
        await query.answer("sᴏʀʀʏ ɴᴏ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.")


# --------------------------------------------------------------------------------------------------------- #

@Hiroko.on_callback_query(filters.regex("music_volume"))
async def volume_sec(_, query : CallbackQuery):
    results = YoutubeSearch(query, max_results=1).to_dict()
    url = f"https://youtube.com{results[0]['url_suffix']}"            
    title = results[0]["title"]            
    duration = results[0]["duration"]
    await query.edit_message_caption(f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({url})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{bsdk}\n",
       reply_markup=button)
                  
# --------------------------------------------------------------------------------------------------------- #

@Hiroko.on_callback_query(filters.regex("volume_50"))
async def volume_50(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    await pytgcalls.change_volume_call(chat_id, 50)
    await query.answer("sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ 50%")
    
@Hiroko.on_callback_query(filters.regex("volume_100"))
async def volume_100(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    await pytgcalls.change_volume_call(chat_id, 100)
    await query.answer("sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ 100%")

@Hiroko.on_callback_query(filters.regex("volume_150"))
async def volume_150(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    await pytgcalls.change_volume_call(chat_id, 150)
    await query.answer("sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ 150%")

@Hiroko.on_callback_query(filters.regex("volume_200"))
async def volume_200(_, query : CallbackQuery):
    chat_id = query.message.chat.id
    await pytgcalls.change_volume_call(chat_id, 200)
    await query.answer("sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ 200%")


# --------------------------------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command("activevoice", prefixes="/"))
async def active_voice(hiroko :Hiroko, message):
    mystic = await message.reply(
        "Fetching active voice chats... Please wait."
    )
    served_chats = await rq.get_active_chats()
    text = ""
    
    for j, chat_id in enumerate(served_chats, start=1):
        try:
            entity = await hiroko.get_chat(chat_id)
            title = entity.title if entity.title else "Private Group"
            if entity.username:
                text += f"{j}. [{title}](https://t.me/{entity.username}) [`{chat_id}`]\n"
            else:
                text += f"{j}. {title} [`{chat_id}`]\n"
        except Exception as e:
            print(f"Error fetching chat info: {e}")
    
    if not text:
        await mystic.edit("No Active Voice Chats found.")
    else:
        await mystic.edit(
            f"**Active Voice Chats:**\n\n{text}"
        )


