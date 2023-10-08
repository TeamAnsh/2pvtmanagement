from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import MONGO_URL
from Hiroko import Hiroko
import datetime
import re


from motor.motor_asyncio import AsyncIOMotorClient as MongoCli



# --------------------------------------------------------------------------------- #


mongo = MongoCli(MONGO_URL)
db = mongo.chatfight

db = db.chatfight


@Hiroko.on_message(filters.group)
async def track_messages(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    current_date = datetime.date.today().isoformat()

    group_collection = db[f"group_{chat_id}"]
    user_document = group_collection.find_one({"user_id": user_id, "date": current_date})

    if user_document:
        # User exists in the database for today, increment their message count
        group_collection.update_one(
            {"_id": user_document["_id"]},
            {"$inc": {"message_count": 1}}
        )
    else:
        # User does not exist for today, create a new document
        new_user_document = {
            "user_id": user_id,
            "date": current_date,
            "message_count": 1
        }
        group_collection.insert_one(new_user_document)


@Hiroko.on_message(filters.command("chatfight"))
async def leaderboard(_, message):
    chat_id = message.chat.id

    # Create an inline keyboard with "Today" and "Overall" buttons
    keyboard = [
        [InlineKeyboardButton("📅 Today", callback_data="today")],
        [InlineKeyboardButton("🏆 Overall", callback_data="overall")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("Choose a leaderboard:", reply_markup=reply_markup)



@Hiroko.on_callback_query(filters.regex(r'^(today|overall)$'))
async def button_click(_, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    group_collection = db[f"group_{chat_id}"]

    if data == 'today':
        top_users = group_collection.find(
            {"date": datetime.date.today().isoformat()}
        ).sort("message_count", -1).limit(10)
        leaderboard_text = "📅 Top 10 users today:\n\n"
    elif data == 'overall':
        top_users = group_collection.aggregate([
            {"$group": {"_id": "$user_id", "total_messages": {"$sum": "$message_count"}}},
            {"$sort": {"total_messages": -1}},
            {"$limit": 10}
        ])
        leaderboard_text = "🏆 Top 10 users overall:\n\n"
    else:
        leaderboard_text = "Invalid choice."

    for rank, user in enumerate(top_users, start=1):
        user_id = user["_id"]
        message_count = user["total_messages"]
        leaderboard_text += f"{rank}. User ID: `{user_id}`, Messages: `{message_count}`\n"

    await callback_query.edit_message_text(text=leaderboard_text)





