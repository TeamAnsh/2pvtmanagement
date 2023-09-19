from config import SUDO_USERS
from pyrogram import filters
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from Hiroko import Hiroko

mongo = MongoCli(MONGO_URL).Rankings

db = mongo["waifu_bot"]

waifu_collection = db["waifus"]



@Hiroko.on_message(filters.command(["addwaifu"]) & filters.user(SUDO_USERS))
async def add_waifu_start(client :Hiroko, message):
    await client.set_value(message.chat.id, "user_state", "waiting_for_photo")
    await client.send_message(
        chat_id=message.chat.id,
        text="Great! Let's add a new waifu. Please send the waifu's photo as a reply to this message.",
    )

@Hiroko.on_message(filters.photo & filters.private)
async def handle_user_input(client :Hiroko, message):
    user_id = message.from_user.id
    user_state = await client.get_value(message.chat.id, "user_state")

    if user_state == "waiting_for_photo":
        await client.set_value(message.chat.id, "waifu_photo", message.photo[-1].file_id)
        await client.set_value(message.chat.id, "user_state", "waiting_for_name")
        await client.send_message(
            chat_id=message.chat.id,
            text="Thanks! Now, please enter the waifu's name.",
        )
    elif user_state == "waiting_for_name":
        await client.set_value(message.chat.id, "waifu_name", message.text)
        await client.set_value(message.chat.id, "user_state", "waiting_for_anime")
        await client.send_message(
            chat_id=message.chat.id,
            text="Got it! Please enter the anime the waifu is from.",
        )
    elif user_state == "waiting_for_anime":
        await client.set_value(message.chat.id, "waifu_anime", message.text)
        await client.set_value(message.chat.id, "user_state", "waiting_for_rarity")
        await client.send_message(
            chat_id=message.chat.id,
            text="Great! Finally, please enter the rarity of the waifu (e.g., common, rare, legendary).",
        )
    elif user_state == "waiting_for_rarity":
        waifu_data = {
            "photo": await client.get_value(message.chat.id, "waifu_photo"),
            "name": await client.get_value(message.chat.id, "waifu_name"),
            "anime": await client.get_value(message.chat.id, "waifu_anime"),
            "rarity": message.text,
        }
        await waifu_collection.insert_one(waifu_data)

        await client.set_value(message.chat.id, "user_state", None)

        await client.send_message(
            chat_id=message.chat.id,
            text="Waifu added successfully! 🌟",
        )




