import requests
import openai
from Hiroko import *
from pyrogram import * 
from pyrogram.types import *
from Hiroko.Helper.database import *


def is_db(chat_id: int):
    x = db.find_one({"chat_id": chat_id})
    if x:
       return True
    return False
    
def ai_on(chat_id: int):
    format = {"chat_id": chat_id, "chatbot": "on"}
    db.insert_one(format)

def ai_off(chat_id: int):
    if is_db:
       db.update_one({"chat_id": chat_id},{"$set":{"chatbot": "off"}})
        




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

      

"""
@Hiroko.on_message(filters.command("chatbot"))
async def chatbot(Hiroko, message):
      user_id = message.from_user.id
      if message.chat.type == enums.ChatType.PRIVATE:
          if not ("on","off") in message.text.split(" ",1)[1]:
             return await message.reply_text("Format: /chatbot on|off")
          elif message.text.split(" ", 1)[1] == "on":
               ai_on(message.chat.id)
               return await message.reply_text("AI Enabled!")
          elif message.text.split(" ",1)[1] == "off":
               ai_off(message.chat.id)
               return await message.reply_text("AI disabled!")      
      else:
        info = await message.chat.get_member(user_id)
        if info.privileges in ("creator", "administrator"):
           if not ("on","off") in message.text.split(" ",1)[1]:
               return await message.reply_text("Format: /chatbot on|off")
           elif message.text.split(" ", 1)[1] == "on":
               ai_on(message.chat.id)
               return await message.reply_text("AI Enabled!")
           elif message.text.split(" ",1)[1] == "off":
               ai_off(message.chat.id)
               return await message.reply_text("AI disabled!")           
        else: return await message.reply("fumk you, you are not admin")

"""

@Hiroko.on_message(filters.text, group=200)
async def chatbot_reply(app, message):
    if is_db:
        bot_id = (await app.get_me()).id
        reply = message.reply_to_message
        if reply and reply.from_user.id == bot_id:
            q = message.text
            try:
                chat_log = session.get('chat_log')
                answer = ask(q, chat_log)
                session['chat_log'] = append_interaction_to_chat_log(Message, answer, chat_log)
                await message.reply(f"{str(answer)}", quote=True)
            except Exception as e:
                return await message.reply("I could not answer this! Let's talk about another topic!")        
    else: 
        return await message.reply_text("Admins Only!")



