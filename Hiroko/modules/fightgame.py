import pyrogram
from config import MONGO_URL, BOT_USERNAME
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Hiroko import Hiroko
import pymongo


client = pymongo.MongoClient(MONGO_URL)
db = client["your_database_name"]
collection = db["user_characters"]


user_profiles = {}

characters_per_page = 6


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
def select_character(_, message):
    user_id = message.from_user.id

    if message.chat.type == enums.ChatType.PRIVATE:          
        btn = InlineKeyboardMarkup([[
            InlineKeyboardButton("ᴘᴍ ᴍᴇ", url=f"http://t.me/{BOT_USERNAME}?start")]])
        message.reply_text(
            f"ʜᴇʏ {message.from_user.mention} ᴘᴍ ᴍᴇ ɪғ ʏᴏᴜ ɪɴᴛʀᴇsᴛᴇᴅ.",
            reply_markup=btn
        )

        if user_id in user_profiles and user_profiles[user_id]["character"] is not None:
            message.reply_text("You've already selected a character. You cannot change it.")
            return

        user_profiles[user_id] = {"character": None, "health": 100}
        user_profiles[user_id]["character_page"] = 0  # Initialize character page to 0
        message.reply_photo(photo="https://telegra.ph/file/061d8efe5247272458cb0.jpg", caption="Welcome to the Jujutsu Kaisen fighting game! Choose your character:", reply_markup=get_character_selection_keyboard(user_id))




def get_character_selection_keyboard(user_id):
    keyboard = []
    user_profile = user_profiles[user_id]
    character_page = user_profile.get("character_page", 0)
    start_index = character_page * characters_per_page
    end_index = start_index + characters_per_page
    characters_to_show = list(characters.keys())[start_index:end_index]

    # Create pairs of buttons
    for i in range(0, len(characters_to_show), 2):
        char_data1 = characters[characters_to_show[i]]
        button1 = InlineKeyboardButton(char_data1["name"], callback_data=f"select_{characters_to_show[i]}")
        
        if i + 1 < len(characters_to_show):
            char_data2 = characters[characters_to_show[i + 1]]
            button2 = InlineKeyboardButton(char_data2["name"], callback_data=f"select_{characters_to_show[i + 1]}")
        else:
            button2 = None

        button_row = [button1, button2] if button2 else [button1]
        keyboard.append(button_row)


    nav_buttons = []
    if character_page > 0:
        nav_buttons.append(InlineKeyboardButton("Previous", callback_data="prev_page"))
    if end_index < len(characters):
        nav_buttons.append(InlineKeyboardButton("Next", callback_data="next_page"))
    keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(keyboard)



@Hiroko.on_callback_query(filters.regex(r"select_(.+)") | filters.regex(r"(prev|next)_page"))
def handle_character_selection(_, query):
    user_id = query.from_user.id
    character_id = query.data.split("_")[1]

    
    if user_profiles[user_id]["character"] is not None:
        query.answer("You already have a character. You cannot change it.")
        return

    
    if character_id in characters:
        user_profiles[user_id]["character"] = character_id
        query.answer(f"You have selected {characters[character_id]['name']} as your character!")

        character_data = {
        "user_id": user_id,
        "character_name": characters[character_id]["name"],        
        }
        collection.insert_one(character_data)


    if query.data == "prev_page":
        user_profiles[user_id]["character_page"] -= 1
    elif query.data == "next_page":
        user_profiles[user_id]["character_page"] += 1
    query.message.edit_caption(caption="Welcome to the Jujutsu Kaisen fighting game! Choose your character:", reply_markup=get_character_selection_keyboard(user_id))




