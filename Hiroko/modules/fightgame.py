import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize the Pyrogram bot
app = Client("jujutsu_kaisen_bot")

# User profiles to store information about players
user_profiles = {}

# Define characters from Jujutsu Kaisen
characters = {
    "yuji": {"name": "Yuji Itadori", "health": 100, "attack": 20},
    "megumi": {"name": "Megumi Fushiguro", "health": 90, "attack": 25},
    # Add more characters here
}

# Handler for /start command to initiate the game
@app.on_message(filters.command("start"))
def start_game(_, message):
    user_id = message.from_user.id
    user_profiles[user_id] = {"character": None, "health": 100}
    message.reply("Welcome to the Jujutsu Kaisen fighting game! Choose your character:", reply_markup=character_selection_keyboard())

# Inline keyboard for character selection
def character_selection_keyboard():
    keyboard = []
    for char_id, char_data in characters.items():
        button = InlineKeyboardButton(char_data["name"], callback_data=f"select_{char_id}")
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)

# Handler for character selection
@app.on_callback_query(filters.regex(r"select_(.+)"))
def select_character(_, query):
    user_id = query.from_user.id
    character_id = query.data.split("_")[1]
    if user_id in user_profiles and character_id in characters:
        user_profiles[user_id]["character"] = character_id
        query.answer(f"You have selected {characters[character_id]['name']} as your character!")

# Handler for battles
@app.on_message(filters.command("fight"))
def fight(_, message):
    user_id = message.from_user.id
    if user_id in user_profiles and user_profiles[user_id]["character"]:
        opponent_id = message.reply_to_message.from_user.id
        if opponent_id in user_profiles and user_profiles[opponent_id]["character"]:
            # Implement battle logic here, calculate damage, and update health
            # Send messages to update users on the battle progress
        else:
            message.reply("Your opponent has not selected a character yet.")
    else:
        message.reply("You need to select a character first. Use /start to begin.")

# Run the bot
if __name__ == "__main__":
    app.run()





