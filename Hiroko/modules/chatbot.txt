import requests
from Hiroko import Hiroko
from pyrogram import filters




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




@Hiroko.on_message(filters.text, group=200)
async def chatbot_reply(hiroko :Hiroko, message):
    BOT_ID = (await Hiroko.get_me()).id
    reply = message.reply_to_message
    if reply and reply.from_user.id == BOT_ID:       
        query = message.text
        response = get_response(message.from_user.id, query)
        await message.reply_text(response["result"]["text"])
    


