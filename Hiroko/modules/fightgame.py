import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko import Hiroko




user_profiles = {}

characters = {
    "user_id": {"name": "Yuji Itadori", "health": 100, "attack": 20},
    "user_id": {"name": "Megumi Fushiguro", "health": 100, "attack": 20},
    "user_id": {"name": "Nobara Kugisaki", "health": 100, "attack": 100},
    "user_id": {"name": "Toge Inumaki", "health": 100, "attack": 20},
    "user_id": {"name": "Panda", "health": 100, "attack": 20},
    "user_id": {"name": "Yuta Okkotsu", "health": 100, "attack": 100},
    "user_id": {"name": "Maki Zenin", "health": 100, "attack": 20},
    "user_id": {"name": "Kinji Hakari", "health": 100, "attack": 20},
    "user_id": {"name": "Kirara Hoshi", "health": 100, "attack": 100},
    "user_id": {"name": "Masamichi Yaga", "health": 100, "attack": 20},
    "user_id": {"name": "Atsuya Kusakabe", "health": 100, "attack": 20},
    "user_id": {"name": "Kiyotaka Ijichi", "health": 100, "attack": 100},
    "user_id": {"name": "Suguru Geto",  "health": 100, "attack": 100},
    "user_id": {"name": "Shoko Ieiri", "health": 100, "attack": 20},
    "user_id": {"name": "Akari Nitta", "health": 100, "attack": 20},
    "user_id": {"name": "Kento Nanami", "health": 100, "attack": 100},
    "user_id": {"name": "Yu Haibara", "health": 100, "attack": 20},
    "user_id": {"name": "Yoshinobu Gakuganji", "health": 100, "attack": 20},
    "user_id": {"name": "Utahime Iori", "health": 100, "attack": 100},
    "user_id": {"name": "Kokichi Muta", "health": 100, "attack": 20},
    "user_id": {"name": "Kasumi Miwa", "health": 100, "attack": 20},
    "user_id": {"name": "Noritoshi Kamo", "health": 100, "attack": 100},
    "user_id": {"name": "Aoi Todo", "health": 100, "attack": 20},
    "user_id": {"name": "Momo Nishimiya", "health": 100, "attack": 20},
    "user_id": {"name": "Kento Nanami", "health": 100, "attack": 100}

}


@Hiroko.on_message(filters.command("character"))
def start_game(_, message):
    user_id = message.from_user.id
    user_profiles[user_id] = {"character": None, "health": 100}
    message.reply("Welcome to the Jujutsu Kaisen fighting game! Choose your character:", reply_markup=character_selection_keyboard())







def character_selection_keyboard():
    keyboard = []
    for char_id, char_data in characters.items():
        button = InlineKeyboardButton(char_data["name"], callback_data=f"select_{char_id}")
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


@Hiroko.on_callback_query(filters.regex(r"select_(.+)"))
def select_character(_, query):
    user_id = query.from_user.id
    character_id = query.data.split("_")[1]
    if user_id in user_profiles and character_id in characters:
        user_profiles[user_id]["character"] = character_id
        query.answer(f"You have selected {characters[character_id]['name']} as your character!")

"""
@Hiroko.on_message(filters.command("fight"))
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


"""



