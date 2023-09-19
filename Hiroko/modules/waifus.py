from pyrogram import Client, filters
import pymongo



mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["waifu_bot"]

waifu_collection = db["waifus"]

# Define a filter to handle the /addwaifu command for sudo user only
@filters.command(["addwaifu"])
def add_waifu_start(client, message):
    if message.from_user.id == sudo_user_id:
        # Set the user's state to "waiting_for_photo"
        client.set_value(message.chat.id, "user_state", "waiting_for_photo")
        client.send_message(
            chat_id=message.chat.id,
            text="Great! Let's add a new waifu. Please send the waifu's photo as a reply to this message.",
        )
    else:
        client.send_message(
            chat_id=message.chat.id,
            text="Sorry, you don't have permission to use this command."
        )

# Handle user input during the /addwaifu process
@app.on_message(filters.photo & filters.private)
def handle_user_input(client, message):
    user_id = message.from_user.id
    user_state = client.get_value(message.chat.id, "user_state")

    if user_state == "waiting_for_photo":
        # Store the waifu photo file_id
        client.set_value(message.chat.id, "waifu_photo", message.photo[-1].file_id)
        client.set_value(message.chat.id, "user_state", "waiting_for_name")
        client.send_message(
            chat_id=message.chat.id,
            text="Thanks! Now, please enter the waifu's name.",
        )
    elif user_state == "waiting_for_name":
        # Store the waifu name
        client.set_value(message.chat.id, "waifu_name", message.text)
        client.set_value(message.chat.id, "user_state", "waiting_for_anime")
        client.send_message(
            chat_id=message.chat.id,
            text="Got it! Please enter the anime the waifu is from.",
        )
    elif user_state == "waiting_for_anime":
        # Store the anime name
        client.set_value(message.chat.id, "waifu_anime", message.text)
        client.set_value(message.chat.id, "user_state", "waiting_for_rarity")
        client.send_message(
            chat_id=message.chat.id,
            text="Great! Finally, please enter the rarity of the waifu (e.g., common, rare, legendary).",
        )
    elif user_state == "waiting_for_rarity":
        # Store the waifu rarity
        waifu_data = {
            "photo": client.get_value(message.chat.id, "waifu_photo"),
            "name": client.get_value(message.chat.id, "waifu_name"),
            "anime": client.get_value(message.chat.id, "waifu_anime"),
            "rarity": message.text,
        }
        waifu_collection.insert_one(waifu_data)

        # Reset user state
        client.set_value(message.chat.id, "user_state", None)

        client.send_message(
            chat_id=message.chat.id,
            text="Waifu added successfully! 🌟",
        )





