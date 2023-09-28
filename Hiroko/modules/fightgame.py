import pyrogram
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Hiroko import Hiroko




user_profiles = {}

characters = {
    "Yuji Itadori": {"name": "Yuji Itadori", "health": 100, "attack": 20},
    "Megumi Fushiguro": {"name": "Megumi Fushiguro", "health": 100, "attack": 20},
    "Nobara Kugisaki": {"name": "Nobara Kugisaki", "health": 100, "attack": 100},
    "Toge Inumaki": {"name": "Toge Inumaki", "health": 100, "attack": 20},
    "Panda": {"name": "Panda", "health": 100, "attack": 20},
    "Yuta Okkotsu": {"name": "Yuta Okkotsu", "health": 100, "attack": 100},
    "Maki Zenin": {"name": "Maki Zenin", "health": 100, "attack": 20},
    "Kinji Hakari": {"name": "Kinji Hakari", "health": 100, "attack": 20},
    "Kirara Hoshi": {"name": "Kirara Hoshi", "health": 100, "attack": 100},
    "Masamichi Yaga": {"name": "Masamichi Yaga", "health": 100, "attack": 20},
    "Atsuya Kusakabe": {"name": "Atsuya Kusakabe", "health": 100, "attack": 20},
    "Kiyotaka Ijichi": {"name": "Kiyotaka Ijichi", "health": 100, "attack": 100},
    "Suguru Geto": {"name": "Suguru Geto",  "health": 100, "attack": 100},
    "Shoko Ieiri": {"name": "Shoko Ieiri", "health": 100, "attack": 20},
    "Akari Nitta": {"name": "Akari Nitta", "health": 100, "attack": 20},
    "Kento Nanami": {"name": "Kento Nanami", "health": 100, "attack": 100},
    "Yu Haibara": {"name": "Yu Haibara", "health": 100, "attack": 20},
    "Yoshinobu Gakuganji": {"name": "Yoshinobu Gakuganji", "health": 100, "attack": 20},
    "Utahime Iori": {"name": "Utahime Iori", "health": 100, "attack": 100},
    "Kokichi Muta": {"name": "Kokichi Muta", "health": 100, "attack": 20},
    "Kasumi Miwa": {"name": "Kasumi Miwa", "health": 100, "attack": 20},
    "Noritoshi Kamo": {"name": "Noritoshi Kamo", "health": 100, "attack": 100},
    "Aoi Todo": {"name": "Aoi Todo", "health": 100, "attack": 20},
    "Momo Nishimiya": {"name": "Momo Nishimiya", "health": 100, "attack": 20},
    "Kento Nanami": {"name": "Kento Nanami", "health": 100, "attack": 100}

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

