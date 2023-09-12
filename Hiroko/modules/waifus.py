import random
from pymongo import MongoClient
from config import MONGO_URL
from pyrogram import Client, filters
from pyrogram.types import InputFile

client = MongoClient(MONGO_URL)
db = client['waifu_database']
waifus_collection = db['waifus']








@Hiroko.on_message(filters.group, group=69)
async def waifu(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in COUNT:
        COUNT[chat_id] = {'count': 0}
    COUNT[chat_id]['count'] += 1
    
    if COUNT[chat_id]['count'] == 100:
        a = random.randint(0, 9)
        b = waifus[a]        
        image = b[2]
        await Hiroko.send_photo(
            message.chat.id,
            photo=InputFile(image),
            caption=f"Wew sexy Waifu Appeared !!!\n\nGuess Her Name And Make Her Your waifu By Using Spell /catch [Her Name]!"
        )






