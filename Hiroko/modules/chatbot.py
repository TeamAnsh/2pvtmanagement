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
promote = ["promote","update"]
demote = ["demote"]






@Hiroko.on_message(filters.command("iroko", prefixes=["h", "H"]) & admin_filter)
async def restriction_hiroko(hiroko :Hiroko, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 3:
        return await message.reply(random.choice(text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        if data[0] in ban:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                await hiroko.ban_chat_member(chat_id, user_id)
                await message.reply("OK, banned!")
        elif data[0] in unban:
            await hiroko.unban_chat_member(chat_id, user_id)
            await message.reply(f"OK, unbanned!")        
        elif data[0] in kick:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                await hiroko.ban_chat_member(chat_id, user_id)
                await hiroko.unban_chat_member(chat_id, user_id)
                await message.reply("get lost! bhga diya bhosdi wale ko") 
        elif data[0] in mute:
            if user_id in SUDO_USERS:
                await message.reply(random.choice(strict_txt))
            else:
                permissions = ChatPermissions(can_send_messages=False)
                await hiroko.set_chat_permissions(chat_id, user_id, permissions)
                await message.reply(f"muted successfully! Disgusting people.") 
        elif data[0] in unmute:
             permissions = ChatPermissions(can_send_messages=True)
             await hiroko.set_chat_permissions(chat_id, user_id, permissions)
             await message.reply(f"Huh, OK, sir!")


        
        elif data[0] in promote:
            if not bot.privileges.can_promote_members:
                return await message.reply("I don't have enough permissions") 
            else:                            
                await hiroko.promote_chat_member(chat_id,user_id,
                   privileges=ChatPrivileges(
                   can_change_info=True,
                   can_invite_users=True,
                   can_delete_messages=True,
                   can_restrict_members=True,
                   can_pin_messages=True,
                   can_manage_chat=True,
                   can_manage_video_chats=True,
                  ),)
                await message.reply(f"OK, sir promoted!")
        elif data[0] in demote:
            if not hiroko.privileges.can_promote_members:
                return await message("I don't have enough permissions")
            else:
                await hiroko.promote_chat_member(chat_id,user_id,
                   privileges=ChatPrivileges(
                   can_change_info=False,
                   can_invite_users=False,
                   can_delete_messages=False,
                   can_restrict_members=False,
                   can_pin_messages=False,
                   can_manage_chat=False,
                   can_manage_video_chats=False,
                    ),)
                await message.reply(f"OK, sir demoted!")


