import requests
import asyncio
from Hiroko import Hiroko
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from requests import get
import datetime




def call_back_in_filter(data):
    return filters.create(lambda flt, _, query: flt.data in query.data,
                          data=data)


def latest():

    url = 'https://subsplease.org/api/?f=schedule&h=true&tz=Japan'
    res = get(url).json()

    k = None
    for x in res['schedule']:
        title = x['title']
        time = x['time']
        try:
            aired = bool(x['aired'])
            title = f"**[{title}](https://subsplease.org/shows/{x['page']})**" if not aired else f"**~~[{title}](https://subsplease.org/shows/{x['page']})~~**"
        except KeyError:
            title = f"**[{title}](https://subsplease.org/shows/{x['page']})**"
        data = f"{title} - {time}"

        if k:
            k = f"{k}\n{data}"
        else:
            k = data

    return k



@Hiroko.on_message(filters.command('latest'))
def lates(_, message):
    mm = latest()
    keyboard = [
        [InlineKeyboardButton("Refresh", callback_data="fook")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message.reply_text(
        f"Today's Schedule:\nTZ: Japan\n{mm}",
        reply_markup=reply_markup
    )


@Hiroko.on_callback_query(call_back_in_filter("fook"))
def callbackk(_, query):
    if query.data == "fk":
        mm = latest()
        time_ = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")
        try:
            query.message.edit_text(
                f"Today's Schedule:\nTZ: Japan\n{mm}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Refresh", callback_data="fk")]
                ])
            )
            query.answer("Refreshed!")
        except:
            query.answer("Refreshed!")




            
@Hiroko.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await Hiroko.send_message(message.chat.id, "waito...")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await Hiroko.send_message(message.chat.id, "waito..")
        photo = "https://apis.xditya.me/write?text=" + name
        await Hiroko.send_photo(message.chat.id, photo=photo)
        await m.delete()



