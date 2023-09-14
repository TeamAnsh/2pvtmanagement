import requests
from Hiroko import Hiroko
from pyrogram import filters, enums
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_URL).Rankings

db = mongo.chatbot


def chatbot_db(chat_id: int):
    x = db.find_one({"chat_id": chat_id})
    if x:
       return True
    return False
    
def chatbot_on(chat_id: int):
    format = {"chat_id": chat_id, "chatbot": "on"}
    db.insert_one(format)

def chatbot_off(chat_id: int):
    if chatbot_db:
       db.update_one({"chat_id": chat_id},{"$set":{"chatbot": "off"}})



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






@Hiroko.on_message(filters.command("chatbot"))
async def chatbot(Hiroko, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if message.chat.type == enums.ChatType.PRIVATE:
        if len(message.text) == 1:
            return await message.reply_text("Format: /chatbot on|off")
        if message.text.split(" ",1)[1] not in ["on","off"]:
            
        elif message.text.split(" ", 1)[1] == "on":
            chatbot_on(chat_id)
            return await message.reply_text("AI Enabled!")
        elif message.text.split(" ",1)[1] == "off":
            chatbot_off(chat_id)
            return await message.reply_text("AI disabled!")      
    else:
        info = await message.chat.get_member(user_id)
        if info.privileges.can_change_info:
            if len(message.text) == 1:
                return await message.reply_text("Format: /chatbot on|off")
            if message.text.split(" ",1)[1] not in ["on","off"]:
                
            elif message.text.split(" ", 1)[1] == "on":       
               chatbot_on(chat_id)
               return await message.reply_text("AI Enabled!")
            elif message.text.split(" ",1)[1] == "off":
               chatbot_off(chat_id)
               return await message.reply_text("AI disabled!")           
            else: return await message.reply("fumk you, you are not admin")




@Hiroko.on_message(filters.text, group=200)
async def chatbot_reply(hiroko :Hiroko, message):
    chat_id = message.chat.id
    if chat_id in chatbot_db:
        BOT_ID = (await Hiroko.get_me()).id
        reply = message.reply_to_message
        if reply and reply.from_user.id == BOT_ID:
            query = message.text
            response = get_response(message.from_user.id, query)
            await message.reply_text(response["result"]["text"])
    else: return await message.reply("sorry sir chatbot is disable")
    


