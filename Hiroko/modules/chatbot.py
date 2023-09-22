import requests
import openai
import random
from config import SUDO_USERS
from Hiroko import *
from pyrogram import * 
from pyrogram.types import *
from Hiroko.Helper.database import *
from pyrogram.enums import ChatMemberStatus, ChatType
from Hiroko.Helper.cust_p_filters import admin_filter





text = (
"hey please don't disturb me.",
"who are you",    
"aap kon ho",
"aap mere owner to nhi lgte ",
"hey tum mera name kyu le rhe ho meko sone do",
"ha bolo kya kaam hai ",
"dekho abhi mai busy hu ",
"hey i am busy",
"aapko smj nhi aata kya ",
"leave me alone",
"dude what happend",
"?",
"nikl lwde",    
)

strict_txt = [
"i can't ban my besties",
"are you serious i am not restirct to my friends",
"fuck you bsdk k mai apne dosto ko kyu kru",
"hey stupid admin ", 
"ha ye phele krlo maar lo ek dusre ki gwaand",   
]
    
openai.api_key = "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"




completion = openai.Completion()


start_sequence = "\nHiroko:"
restart_sequence = "\nPerson:"
session_prompt = chatbot_txt

session = {}

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'

      

@Hiroko.on_message(filters.text, group=200)
async def chatbot_reply(hiroko :Hiroko, message):
    bot_id = (await hiroko.get_me()).id
    reply = message.reply_to_message
    if reply and reply.from_user.id == bot_id:
        q = message.text
        try:
            chat_log = session.get('chat_log')
            answer = ask(q, chat_log)
            session['chat_log'] = append_interaction_to_chat_log(Message, answer, chat_log)
            await message.reply(f"{str(answer)}", quote=True)
        except Exception as e:
            return await message.reply("I can't answer that.")        



ban = ["ban","spammed","rival"]
unban = ["unban","free"]
mute = ["mute","silent"]
unmute = ["unmute","speak"]
kick = ["kick", "promotion"]




@Hiroko.on_message(filters.command("iroko", prefixes=["h", "H"]) & admin_filter)
async def restriction_hiroko(client: Hiroko, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = reply.from_user.id

    if len(message.text) < 10:
        return await message.reply(random.choice(text))

    nono = message.text.split(maxsplit=1)[1]
    data = nono.split(" ")
    banned, unbanned, muted, unmuted, kicked = data, data, data, data, data

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("**Are you stupid? I can't ban in private messages.**")

    if reply:
        user_stats = await client.get_chat_member(chat_id, user_id)
        if banned in ban:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                await client.ban_chat_member(chat_id, user_id)
                await message.reply(f"OK, banned!")
        elif unbanned in unban:
            await client.unban_chat_member(chat_id, user_id)
            await message.reply(f"OK, unbanned!")
        elif muted in mute:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                permissions = ChatPermissions(can_send_messages=False)
                await client.set_chat_permissions(chat_id, user_id, permissions)
                await message.reply(f"Muted successfully! Disgusting people.")
        elif unmuted in unmute:
            permissions = ChatPermissions(can_send_messages=True)
            await client.set_chat_permissions(chat_id, user_id, permissions)
            await message.reply(f"Huh, OK, sir!")
        elif kicked in kick:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                await client.ban_chat_member(chat_id, user_id)
                await client.unban_chat_member(chat_id, user_id)
                await message.reply(f"Kicked successfully! Bhen k lund.")

