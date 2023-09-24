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
from lexica import Client





hiroko_text = [
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
]

strict_txt = [
"i can't restrict against my besties",
"are you serious i am not restrict to my friends",
"fuck you bsdk k mai apne dosto ko kyu kru",
"hey stupid admin ", 
"ha ye phele krlo maar lo ek dusre ki gwaand",  
"i can't hi is my closest friend",
"i love him please don't restict this user try to usertand "
]


# ========================================= #


def main(prompt: str) -> str:
    client = Client()
    response = client.palm(prompt)
    return response["content"].strip()


# ========================================= #


api_key = "BLUE-AI-25154789-6280048819-123-white-kazu-6280048819"

def get_response(user_id, query):
    params = {
        "user_id": user_id,
        "query": query,
        "BOT_ID": 6632922889
    }

    headers = {
        "api_key": api_key
        
    }

    response = requests.get("https://blue-api.vercel.app/chatbot1", params=params, headers=headers)
    return response.json()



# ========================================= #

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


# ========================================= #






@Hiroko.on_message(filters.text, group=200)
async def chatbot_reply(hiroko: Hiroko, message):
    bot_id = 6632922889
    reply = message.reply_to_message
    if reply and reply.from_user.id == bot_id:
        query = message.text
        try:
            chat_log = session.get('chat_log')
            answer = ask(query, chat_log)
            session['chat_log'] = append_interaction_to_chat_log(Message, answer, chat_log)
            await message.reply(str(answer), quote=True)
        except Exception as e:
            print(f"Error: {e}")
            try:
                response = main(query)
                return await message.reply(response) 
            except Exception as e:
                print(f"Error: {e}")
                try:               
                    response = get_response(message.from_user.id, query)
                    await message.reply_text(response["result"]["text"])
                except Exception as e:
                    print(f"Error: {e}")



# ========================================= #


ban = ["ban","boom"]
unban = ["unban",]
mute = ["mute","silent","shut"]
unmute = ["unmute","speak","free"]
kick = ["kick", "out","nikaal"]
promote = ["promote","update"]
demote = ["demote"]




# ========================================= #


@Hiroko.on_message(filters.command("iroko", prefixes=["h", "H"]) & admin_filter)
async def restriction_hiroko(hiroko :Hiroko, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(hiroko_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")
    
    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDO_USERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await hiroko.ban_chat_member(chat_id, user_id)
                    await message.reply("OK, banned!")
        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await hiroko.unban_chat_member(chat_id, user_id)
                await message.reply(f"OK, unbanned!") 
        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDO_USERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await hiroko.ban_chat_member(chat_id, user_id)
                    await hiroko.unban_chat_member(chat_id, user_id)
                    await message.reply("get lost! bhga diya bhosdi wale ko") 
        for muted in data:
            print(f"present {muted}") 
            if muted in mute:
                if user_id in SUDO_USERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await hiroko.set_chat_permissions(chat_id, user_id, permissions)
                    await message.reply(f"muted successfully! Disgusting people.") 
        for unmuted in data:
            print(f"present {unmuted}")            
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await hiroko.set_chat_permissions(chat_id, user_id, permissions)
                await message.reply(f"Huh, OK, sir!")







        
        """
        for promoted in data:
        
        print(f"present {promoted}")
        elif data[0] in promote:
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
        
            if not admin_check.privileges.can_promote_members:
                return await message.reply("I don't have enough permissions") 
            else:
                if admin_check.can_promote_members:
                    await message.chat.promote_member(user.id, privileges=ChatPrivileges(
                      can_change_info=True,
                      can_invite_users=True,
                      can_delete_messages=True,
                      can_restrict_members=True,
                      can_pin_messages=True,
                      can_promote_members=False,
                      can_manage_chat=True,
                      can_manage_video_chats=True,
                  ))
                await message.reply(f"OK, sir promoted!")
        for demoted in data:
        print(f"present {demoted}")    
    
        elif data[0] in demote:
            admin_check = await Hiroko.get_chat_member(chat_id, user_id)
        
            if not admin_check.privileges.can_promote_members:
                return await message("I don't have enough permissions")
            else:
                if admin_check.can_promote_members:
                    await message.chat.promote_member(user.id, privileges=ChatPrivileges(
                      can_change_info=False,
                      can_invite_users=False,
                      can_delete_messages=False,
                      can_restrict_members=False,
                      can_pin_messages=True,
                      can_promote_members=False,
                      can_manage_chat=False,
                      can_manage_video_chats=False,
                   ))
                await message.reply(f"OK, sir demoted!")
"""



# ========================================= #





