import asyncio
import random
from config import BOT_USERNAME, OWNER_ID
from pyrogram import Client, filters, enums
from Hiroko import Hiroko
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton





# ------------------------------------------------------------------------------- #

START_IMG = (
"https://graph.org/file/f035f0e34969c14ae2e8c.jpg",
"https://graph.org/file/68227791cf9273fbede7a.jpg",
"https://graph.org/file/d91ec80b019d43082965d.jpg",
"https://graph.org/file/d6ae49af114fa50d5ba89.jpg",
"https://graph.org/file/30f6cc0b6251afe5c4153.jpg",
"https://telegra.ph/file/0214edaebad6ef6d69c1d.jpg",
"https://telegra.ph/file/f658925a255bea26efaa4.jpg",
"https://telegra.ph/file/235e4c7e9dd0c48bac638.jpg",

)



# ------------------------------------------------------------------------------- #

START_TEXT = """
**ʜᴇʏ ᴛʜᴇʀᴇ [{}](tg://user?id={}) ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ !**
━━━━━━━━━━━━━━━━━━━━━━**
๏ ɪ ᴀᴍ ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴀɴᴅ ɪ ʜᴀᴠᴇ sᴘᴇᴄɪᴀʟ ғᴇᴀᴛᴜʀᴇs
๏ ɪ ᴀᴍ ᴅɪғғᴇʀᴇɴᴛ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛs

๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs**
"""


# ------------------------------------------------------------------------------- #

HELP_TEXT = """**
» ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴄᴏᴏʟ ᴏʀ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs 
"""

DEVS_SECTION = """
** ˹ʜɪꝛᴏᴋᴏ ꝛᴏʙᴏᴛ˼ ᴅᴇᴠs ᴏʀ ᴍᴀɪɴᴛᴀɪɴᴇʀ sᴇᴄᴛɪᴏɴ**
"""

# ------------------------------------------------------------------------------- #

hiroko_buttons = [              
                [
                    InlineKeyboardButton("ᴀғᴋ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴀᴄᴛɪᴏɴ", callback_data="maintainer_"),
                    InlineKeyboardButton("ғᴜɴ", callback_data="maintainer_")
                ],
                [
                    InlineKeyboardButton("ɢᴀᴍᴇs", callback_data="maintainer_"),   
                    InlineKeyboardButton("ɪᴍᴀɢᴇs", callback_data="maintainer_"),
                    InlineKeyboardButton("ɢʀᴏᴜᴘs", callback_data="maintainer_")
                ],
                [
                    InlineKeyboardButton("ᴄʜᴀᴛʙᴏᴛ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴍɪsᴄ", callback_data="maintainer_"),
                    InlineKeyboardButton("ɪᴍᴘᴏsᴛᴇʀ", callback_data="maintainer_")
                ],
                [
                    InlineKeyboardButton("ᴄʜᴀᴛɢᴘᴛ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ᴀɪ", callback_data="maintainer_"),
                    InlineKeyboardButton("ᴍᴜsɪᴄ", callback_data="maintainer_")
                ],
                [
                    InlineKeyboardButton("ᴡᴇʟᴄᴏᴍᴇ", callback_data="maintainer_"),   
                    InlineKeyboardButton("ɴᴏᴛᴇs", callback_data="maintainer_"),
                    InlineKeyboardButton("ғɪʟᴛᴇʀs", callback_data="maintainer_")
                ],
                [
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),
                    InlineKeyboardButton("⟲ ᴄʟᴏꜱᴇ ⟳", callback_data="close_data")
                ]
                ]


back_buttons  = [[
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="help_"),                    
                ]]


devs_buttons  = [[
                    InlineKeyboardButton("ᴋɪᴛᴏ", url="https://t.me/KIRITO1240"),
                    InlineKeyboardButton("ɪᴍᴏʀᴛᴀʟ", url="https://t.me/ImmortalsKingX"),                    
                ],
                [
                    InlineKeyboardButton("ɪsʜɪᴋᴋɪ", url="https://t.me/ishikki_Akabane"),
                    InlineKeyboardButton("ʟᴇᴠɪ", url="https://t.me/LeviAckerman1709"), 
                ],
                [
              
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),                    
                ]  
                ]

# ------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client: Client, message: Message):
    buttons =  [
            [
                InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/DevsOops"),
                InlineKeyboardButton("🎓 ᴍᴀɪɴᴛᴀɪɴᴇʀ", callback_data="hiroko_devs"),
            ],
            [
                InlineKeyboardButton("📚 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 📚", callback_data="help_")
            ]    
        ]
                                    
    reply_markup = InlineKeyboardMarkup(buttons)
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_photo(
            photo=random.choice(START_IMG),
            caption=START_TEXT.format(message.from_user.first_name, message.from_user.id),
            reply_markup=reply_markup
        )
    else:
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("ᴘᴍ ᴍᴇ", url=f"http://t.me/{BOT_USERNAME}?start")]])
        await message.reply(
            f"ʜᴇʏ {message.from_user.mention} ᴘᴍ ᴍᴇ ɪғ ʏᴏᴜ ɪɴᴛʀᴇsᴛᴇᴅ.",
            reply_markup=btn
        )



# ------------------------------------------------------------------------------- #

@Hiroko.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="home_":
        buttons =  [
            [
                InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
            [
                InlineKeyboardButton("✨ sᴜᴘᴘᴏʀᴛ ✨", url="https://t.me/TheNixaSupport"),
                InlineKeyboardButton("🎓 ᴍᴀɪɴᴛᴀɪɴᴇʀ", callback_data="hiroko_devs"),
            ],
            [
                InlineKeyboardButton("📚 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 📚", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                START_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


# ------------------------------------------------------------------------------- #
        
    elif query.data=="help_":        
        reply_markup = InlineKeyboardMarkup(hiroko_buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass



    elif query.data=="hiroko_devs":        
        reply_markup = InlineKeyboardMarkup(devs_buttons)
        try:
            await query.edit_message_text(
                DEVS_SECTION.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
  
# ------------------------------------------------------------------------------- #

    elif query.data=="maintainer_":
            await query.answer(("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ "), show_alert=True)

  
# ------------------------------------------------------------------------------- #
 
    elif query.data=="close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
          

