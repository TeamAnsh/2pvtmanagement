import asyncio
from Hiroko import Hiroko
from config import MONGO_URL
from datetime import datetime, timedelta
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_URL)
db = mongo.chatfight


message_collection = None



@Hiroko.on_message(filters.command("remember"))
async def remember_message(_, message):
    global message_collection
    if not message_collection:
        message_collection = db["messages"]

    # Store the message text and timestamp in the database
    message_text = message.text[10:]  # Remove the "/remember " part
    timestamp = datetime.now()
    message_data = {
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "message_text": message_text,
        "timestamp": timestamp
    }
    await message_collection.insert_one(message_data)
    await message.reply_text("Message remembered!")



@Hiroko.on_message(filters.command("recall"))
async def recall_messages(_, message):
    if not message_collection:
        await message.reply_text("No messages have been remembered yet.")
        return

    # Calculate the time frame (in hours) for recalling messages
    try:
        hours = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply_text("Invalid command usage. Use /recall [hours] to recall messages.")
        return

    # Calculate the timestamp threshold (messages newer than this timestamp will be recalled)
    timestamp_threshold = datetime.now() - timedelta(hours=hours)

    # Query the database for remembered messages within the time frame
    recalled_messages = []
    async for msg_data in message_collection.find({"timestamp": {"$gt": timestamp_threshold}}):
        recalled_messages.append(msg_data["message_text"])

    if recalled_messages:
        # Send the recalled messages as a reply
        await message.reply_text("\n".join(recalled_messages))
    else:
        await message.reply_text("No messages found within the specified time frame.")


# Function to remind users of messages after a specified time
async def remind_users():
    while True:
        if message_collection:
            current_time = datetime.now()
            # Calculate the timestamp threshold (messages to remind)
            timestamp_threshold = current_time - timedelta(hours=9)
            async for msg_data in message_collection.find({"timestamp": {"$lte": timestamp_threshold}}):
                user_id = msg_data["user_id"]
                chat_id = msg_data["chat_id"]
                message_text = msg_data["message_text"]
                await app.send_message(chat_id, f"Reminder for User {user_id}:\n{message_text}")
                await message_collection.delete_one({"_id": msg_data["_id"]})
        await asyncio.sleep(60)  # Check for reminders every 60 seconds

import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# Initialize the Pyrogram Client
app = Client("my_account")

# MongoDB Configuration
MONGO_URL = "mongodb://localhost:27017/"
mongo = MongoCli(MONGO_URL)
db = mongo.chatfight

# Define global variables
message_collection = None

# Function to remember messages
async def remember_message(user_id, chat_id, message_text):
    if not message_collection:
        message_collection = db["messages"]

    # Store the message text and timestamp in the database
    timestamp = datetime.now()
    message_data = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message_text": message_text,
        "timestamp": timestamp
    }
    await message_collection.insert_one(message_data)

# Function to remind users of messages
async def remind_users():
    while True:
        if message_collection:
            current_time = datetime.now()
            # Calculate the timestamp threshold (messages to remind)
            timestamp_threshold = current_time - timedelta(hours=9)
            async for msg_data in message_collection.find({"timestamp": {"$lte": timestamp_threshold}}):
                user_id = msg_data["user_id"]
                chat_id = msg_data["chat_id"]
                message_text = msg_data["message_text"]
                await app.send_message(chat_id, f"Reminder for User {user_id}:\n{message_text}")
                await message_collection.delete_one({"_id": msg_data["_id"]})
        await asyncio.sleep(60)  # Check for reminders every 60 seconds

# Run the Pyrogram Client
@app.on_message(filters.text)
async def auto_remember_message(_, message):
    # Automatically remember messages from users
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_text = message.text
    await remember_message(user_id, chat_id, message_text)

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(remind_users())
    app.run()



