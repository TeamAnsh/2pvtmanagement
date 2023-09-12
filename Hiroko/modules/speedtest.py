import os
import wget
import asyncio
import speedtest
from PIL import Image
from Hiroko import Hiroko
from pyrogram.types import Message
from pyrogram import filters, Client as client

# ------------------------------------------------------------------------------- #

def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("**⇆ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...**")
        test.download()
        m = m.edit("**⇆ ʀᴜɴɴɪɴɢ ᴜᴩʟᴏᴀᴅ sᴩᴇᴇᴅᴛᴇsᴛ...**")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("**↻ sʜᴀʀɪɴɢ sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs...**")
    except Exception as e:
        return m.edit(e)
    return result

# ------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["speedtest"], prefixes=["/", "!"]))
async def speedtest_function(client, message):
    m = await message.reply_text("💫 ᴛʀʏɪɴɢ ᴛᴏ ᴄʜᴇᴄᴋ ᴜᴩʟᴏᴀᴅ ᴀɴᴅ ᴅᴏᴡɴʟᴏᴀᴅ sᴩᴇᴇᴅ...")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f""" **sᴩᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs** 
    
<u>**❥͜͡ᴄʟɪᴇɴᴛ :**</u>
**» ɪsᴩ :** {result['client']['isp']}
**» ᴄᴏᴜɴᴛʀʏ :** {result['client']['country']}
  
<u>**❥͜͡sᴇʀᴠᴇʀ :**</u>
**» ɴᴀᴍᴇ :** {result['server']['name']}
**» ᴄᴏᴜɴᴛʀʏ :** {result['server']['country']}, {result['server']['cc']}
**» sᴩᴏɴsᴏʀ :** {result['server']['sponsor']}
**» ʟᴀᴛᴇɴᴄʏ :** {result['server']['latency']}  
**» ᴩɪɴɢ :** {result['ping']}"""
    msg = await Hiroko.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
    
# ------------------------------------------------------------------------------- #

