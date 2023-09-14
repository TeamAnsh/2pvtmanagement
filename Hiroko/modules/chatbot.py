import requests
from Hiroko import Hiroko
from pyrogram import Client, filters

api_key = "BLUE-AI-blue-789-kafu-chino-5030730429-63001503-5030730429"  # Replace with your API key

def get_response(user_id, query):
    params = {
        "user_id": user_id,    
        "query": query          
    }

    headers = {
        "api_key": api_key
    }

    response = requests.get("https://blue-api.vercel.app/chatbot1", params=params, headers=headers)
    return response.text



@Hiroko.on_message(filters.command("chat", prefixes="/"))
def chat(client, message):
    query = message.text.split("/chat", maxsplit=1)[1].strip()
    response = get_response(message.from_user.id, query)
    message.reply_text(response)




