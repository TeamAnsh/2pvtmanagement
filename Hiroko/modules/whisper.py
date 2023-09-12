from pyrogram import filters
from pyrogram.types import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from pyrogram import enums
from Hiroko import Hiroko


@Hiroko.on_message(filters.command("whisper", COMMAND_HANDLER))
async def startmsg(hiroko :Hiroko, message):
   text = f"""
👋 Hi {message.from_user.mention}

❓ How to use this bot in inline:

`@{hiroko.me.username} Hi @AnonDeveloper`
`@{hiroko.me.username} Hi @all`

"""
   key = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ("TRY NOW", switch_inline_query='Hi @AnonDeveloper') ]]
   )
   await message.reply(text, reply_markup=key, quote=True)



@Hiroko.on_inline_query(filters.regex("@"))
async def whisper(hiroko :Hiroko, iquery):
    user = iquery.query.split("@")[1]
    if " " in user: return 
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
      text = "🎊 This wisper for all"
      username = "all"
    else:
      try:
       get = await hiroko.get_chat(user)
       user = get.id
       username = get.username
      except Exception:
        pass
      text = f"**🔒 Secret whisper for ( @{username} ) .ا**"
    send = await hiroko.send_message(CHANNEL_ID, query)
    reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("📪 Show whisper", callback_data=f"{send.id}catch{user}from{user_id}")
      ]]
    )
    await iquery.answer(
      results=[
       InlineQueryResultArticle(
          title=f"📪 Send whisper for {username}",
          url="http://t.me/DevOops",
          input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode=enums.ParseMode.MARKDOWN 
          ),
          reply_markup=reply_markup
       )
      ],
      cache_time=1
    )


@Hiroko.on_inline_query()
async def whisper(hiroko :Hiroko, query):
    text = f"""
❓ How to use this bot in inline:

@{app.me.username} Hi @AnonDeveloper
@{app.me.username} Hi @all
"""
    await query.answer(
        results=[
            InlineQueryResultPhoto(
                title="🔒 Type the whisper + username",
                photo_url='https://t.me/AnonDeveloper',
                description=f'@{app.me.username} Hello @AnonDeveloper',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🔗", url='t.me/DevOops')]]),
                input_message_content=InputTextMessageContent(text)
            ),
        ],
        cache_time=1
    )


@Hiroko.on_callback_query(filters.regex("catch"))
async def get_whisper(hiroko :Hiroko,query):
    sp = query.data.split("catch")[1]
    user = sp.split("from")[0]
    from_user = int(sp.split("from")[1])
    reply_markup = InlineKeyboardMarkup(
      [
      [
        InlineKeyboardButton("📭 Show whisper", callback_data=query.data)
      ],
      [
        InlineKeyboardButton("🗑️", callback_data=f"DELETE{from_user}")
      ],
      ]
    )
    if user == "all":
       msg = await hiroko.get_messages(CHANNEL_ID, int(query.data.split("catch")[0]))
       await query.answer(msg.text, show_alert=True)
       try:
         await query.edit_message_reply_markup(
           reply_markup
         )
       except:
         pass
       return 
    
    else:
      if str(query.from_user.id) == user:
        msg = await hiroko.get_messages(CHANNEL_ID, int(query.data.split("catch")[0]))
        await query.answer(msg.text, show_alert=True)
        try:
         await query.edit_message_reply_markup(
           reply_markup
         )
        except:
         pass
        return 

      if query.from_user.id == from_user:
        msg = await hiroko.get_messages(CHANNEL_ID, int(query.data.split("catch")[0]))
        await query.answer(msg.text, show_alert=True)
        return
      
      else:
        await query.answer("🔒 This whisper it's not for you .", show_alert=True)
        return 


                                     
@Hiroko.on_callback_query(filters.regex("DELETE"))
async def del_whisper(hiroko :Hiroko,query):
   user = int(query.data.split("DELETE")[1])
   if not query.from_user.id == user:
     return await query.answer("❓ Only the sender can use this button .")
   
   else:
     reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("DEV. 🔗", url="https://t.me/AnonDeveloper")
      ]]
    )
     await query.edit_message_text(f"**🗑️ This whisper was deleted by ( {query.from_user.mention} ) .**",
       reply_markup=reply_markup
     )
     



