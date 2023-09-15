from pyrogram import Client, filters

# Define your API credentials and session name
api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
session_name = "your_session_name"

# Create a Pyrogram client
app = Client(session_name, api_id, api_hash)

# Define the URL
pi_url = "https://pi.ai/talk"

# Function to interact with Pi AI and get a response
async def chat_with_pi(message_text):
    try:
        # Prepare the payload with the message
        data = {
            "message": message_text
        }

        # Send a POST request to the chat API
        response = await app.session.post(pi_url, data=data)

        if response.status_code == 200:
            # Extract and return the response text
            response_data = await response.json()
            return response_data.get("reply", "No response received.")
        else:
            return "Error: Unable to communicate with the chat service."

    except Exception as e:
        return f"Error: {str(e)}"

# Define a command handler for handling incoming messages
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hi there! Send me a message, and I'll chat with Pi AI.")

# Define a message handler for handling user messages
@Hiroko.on_message(filters.text)
async def handle_message(client, message):
    user_input = message.text
    response = await chat_with_pi(user_input)
    await message.reply(response)



    
