import requests
from pyrogram import Client, filters

api_key = "BLUE-AI-25154789-6280048819-123-white-kazu-6280048819"  

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



@Natasha.on_message(filters.command("chat", prefixes="/"))
def chat(client, message):
    query = message.text.split("/chat", maxsplit=1)[1].strip()
    response = get_response(message.from_user.id, query)
    message.reply_text(response)




