import aiohttp
from pyrogram import filters
from Hiroko import Hiroko

session = aiohttp.ClientSession()

pi_url = "https://pi.ai/"



# Function to interact with Pi AI and get a response
async def chat_with_pi(message_text):
    try:
        # Prepare the payload with the message
        data = {
            "message": message_text
        }

        # Send a POST request to the chat API
        async with session.post(pi_url, data=data) as response:
            if response.status == 200:
                # Extract and return the response text
                response_data = await response.json()
                return response_data.get("reply", "No response received.")
            else:
                return "Error: Unable to communicate with the chat service."

    except Exception as e:
        return f"Error: {str(e)}"

@Hiroko.on_message(filters.text)
async def handle_message(_, message):
    user_input = message.text
    response = await chat_with_pi(user_input)
    await message.reply(response)




