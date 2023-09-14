import requests
from Hiroko import Hiroko
from pyrogram import Client, filters



api_key = "BLUE-AI-25154789-6280048819-123-white-kazu-6280048819"  # Replace with your API key


def get_response(user_id, query):
    params = {
        "user_id": user_id,     # Replace with the user ID you want to use
        "query": query          # Replace with your query
    }

    headers = {
        "api_key": api_key
    }

    response = requests.get("https://blue-api.vercel.app/chatbot1", params=params, headers=headers)
    return response.text



@Hiroko.on_message(filters.command("chat", prefixes="/"))
def chat(client, message):
    reply = message.reply_to_message
    query = message.text.split("/chat", maxsplit=1)[1].strip()
    response = get_response(message.from_user.id, query)
    result = response.json()
    if not reply:
      await message.reply_text(result["result"]["text"])
    else:
        await reply.reply(result["result"]["text"])
    




