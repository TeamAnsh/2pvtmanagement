import json
import asyncio
import datetime, pymongo
import config, random
from Hiroko import Hiroko
from Hiroko.modules.ping import get_readable_time
from Hiroko import BOT_ID
from config import SUDO_USERS as SUPREME_USERS
from pyrogram import filters
from Hiroko.modules.games import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

# --------------------------------------------------------------------------------- #

photo = [
"https://graph.org/file/2fc37c68163780e31599f.jpg",
"https://graph.org/file/3cc07627bdec5f5afab1c.jpg",
"https://graph.org/file/809fe233d8f7c29c6fd69.jpg",
"https://graph.org/file/677619500837cd3190c6d.jpg",
"https://graph.org/file/2a4d6cfdf60a38130aad2.jpg",
"https://graph.org/file/066ed5867fe94c333c0b6.jpg",
"https://graph.org/file/bd06b509e025bc656766d.jpg",
"https://graph.org/file/cd33fd3d193ac98486eff.jpg",
"https://graph.org/file/9ffb36ba7d53b7894eaba.jpg",
"https://graph.org/file/fe6dc66f7968ea69dcec0.jpg",
"https://graph.org/file/917d3b7324a056d66a8cb.jpg",
"https://graph.org/file/4f46ebdf26f703f1d5e93.jpg",
"https://graph.org/file/b3d7c31922a85e94e9627.jpg",
"https://graph.org/file/82560acb529e63c9ddb94.jpg",

]






# --------------------------------------------------------------------------------- #


mongo = MongoCli(MONGO_URL)
db = mongo.Anonymous

gamesdb = db.games


# --------------------------------------------------------------------------------- #


async def create_account(user_id,user_name):
  dic = {
  'user_id' : user_id,
    "username" : user_name,
    'coins' : 50000,
  }
  return gamesdb.insert_one(dic)

# --------------------------------------------------------------------------------- #

async def is_player(user_id):
  return bool(await gamesdb.find_one({"user_id" : user_id}))

# --------------------------------------------------------------------------------- #

async def user_wallet(user_id):
    player = await gamesdb.find_one({"user_id" : user_id})
    if not player:
        return 0
    return player['coins']

# --------------------------------------------------------------------------------- #
 
async def write_last_collection_time_today(user_id, time):
    await gamesdb.update_one({'user_id' : user_id},{'$set' : {'last_date' : time}},upsert=True)

# --------------------------------------------------------------------------------- #

async def read_last_collection_time_today(user_id):
    user = await gamesdb.find_one({'user_id' : user_id})
    try:
        collection_time = user['last_date']  
    except : 
        collection_time = None
    if collection_time:  
        return datetime.datetime.fromtimestamp(collection_time)
    else:
        return None

# --------------------------------------------------------------------------------- #

async def can_collect_coins(user_id):
    last_collection_time = await read_last_collection_time_today(user_id)
    if last_collection_time is None:
        return (True,True)
    current_time = datetime.datetime.now()
    time_since_last_collection = current_time - last_collection_time
    return (time_since_last_collection.total_seconds() >= 24 * 60 * 60,24 * 60 * 60 - time_since_last_collection.total_seconds())
  
# --------------------------------------------------------------------------------- #
  
async def write_last_collection_time_weekly(user_id, time):
    await gamesdb.update_one({'user_id' : user_id},{'$set' : {'last_collection_weekly' : time}},upsert=True)

# --------------------------------------------------------------------------------- #

async def read_last_collection_time_weekly(user_id):
    user = await gamesdb.find_one({'user_id' : user_id})
    try:
        collection_time = user['last_collection_weekly']  
    except : 
        collection_time = None
    if collection_time:  
        return datetime.datetime.fromtimestamp(collection_time)
    else:
        return None
        
# --------------------------------------------------------------------------------- #
           
async def find_and_update(user_id,username):
    user= await gamesdb.find_one({"user_id" : user_id})
    if not user:
        return
    old_username = user["username"].lower()
    if old_username != username.lower():
        return await gamesdb.update_one({'user_id' : user_id},{'$set' : {'username' : username}})


# --------------------------------------------------------------------------------- #

async def can_collect(user_id):
    last_collection_time = await read_last_collection_time_weekly(user_id)
    if last_collection_time is None:
        return (True,True)
    current_time = datetime.datetime.now()
    time_since_last_collection = current_time - last_collection_time
    return (time_since_last_collection.total_seconds() >= 7 * 24 * 60 * 60,7 * 24 * 60 * 60 - time_since_last_collection.total_seconds())


# --------------------------------------------------------------------------------- #


async def get_user_won(emoji,value):
    if emoji in ['🎯','🎳']:
        if value >= 4:
            u_won = True
        else:
            u_won = False
    elif emoji in ['🏀','⚽'] :
        if value >= 3:
            u_won = True
        else:
            u_won = False
    return u_won

# --------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["bonus","daily"]))
async def _daily(client,message):
    user_id = message.from_user.id
    if not await is_player(user_id):
        await create_account(user_id,message.from_user.username)
    coins = await user_wallet(user_id)
    x,y = await can_collect_coins(user_id)
    if x is True:
        await gamesdb.update_one({'user_id' : user_id},{'$set' : {'coins' : coins + 10000}},upsert=True)
        await write_last_collection_time_today(user_id,datetime.datetime.now().timestamp())
        return await message.reply_photo(photo=random.choice(photo), caption="🎁 Yᴏᴜ ʜᴀᴠᴇ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ᴅᴀɪʟʏ ʙᴏɴᴜs ᴏғ 10,𝟶𝟶𝟶 ᴅᴀʟᴄs!\n• ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}`ᴅᴀʟᴄs".format(coins+10000))    
    await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴄᴀɴ ᴄʟᴀɪᴍ ʏᴏᴜʀ ᴅᴀɪʟʏ ʙᴏɴᴜs ɪɴ ᴀʀᴏᴜɴᴅ `{0}`".format(get_readable_time(y)))  
    
    
 # --------------------------------------------------------------------------------- #
   
@Hiroko.on_message(filters.command(["rewards","weekly"]))
async def _weekly(client,message):
    user_id = message.from_user.id
    if not await is_player(user_id):
        await create_account(user_id,message.from_user.username)
    coins = await user_wallet(user_id)
    x,y = await can_collect(user_id)
    if x is True:
        await gamesdb.update_one({'user_id' : user_id},{'$set' : {'coins' : coins + 50000}},upsert=True)
        await write_last_collection_time_weekly(user_id,datetime.datetime.now().timestamp())
        return await message.reply_photo(photo=random.choice(photo), caption="🎁 ʏᴏᴜ ʜᴀᴠᴇ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ᴡᴇᴇᴋʟʏ ʙᴏɴᴜs ᴏғ 50,000 ᴅᴀʟᴄs!\n• ᴛᴏᴛᴀʟ ᴅᴀʟᴄs ✑ `{0:,}` ᴅᴀʟᴄs".format(coins+50000))    
    await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴄᴀɴ ᴄʟᴀɪᴍ ʏᴏᴜʀ ᴡᴇᴇᴋʟʏ ʙᴏɴᴜs ɪɴ ᴀʀᴏᴜɴᴅ `{0}`".format(get_readable_time(y)))
                         
                             
  # --------------------------------------------------------------------------------- #
                           
async def can_play(tame,tru):
  current_time = datetime.datetime.now()
  time_since_last_collection = current_time - datetime.datetime.fromtimestamp(tame)
  x = tru - time_since_last_collection.total_seconds()
  if str(x).startswith('-'):
      return 0
  return x
  

BET_DICT = {}
DART_DICT = {}
BOWL_DICT = {}
BASKET_DICT = {}
TRIVIA_DICT = {}


 # --------------------------------------------------------------------------------- #


@Hiroko.on_message(filters.command(["bet","toss"]))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)
  if user.id not in BET_DICT.keys():
      BET_DICT[user.id] = None     
  if BET_DICT[user.id]:
      x= await can_play(BET_DICT[user.id],12)
      print(x)
      if int(x) != 0:
        return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ʙᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ {get_readable_time(x)}.')     
  possible = ['h','heads','tails','t','head','tail']
  if len(message.command) < 3:
      return await message.reply_photo(photo=random.choice(photo), caption="✑ ᴜsᴀɢᴇ : /bet [ᴀᴍᴏᴜɴᴛ] [ʜᴇᴀᴅs/ᴛᴀɪʟs]")
  to_bet = message.command[1]
  cmd = message.command[2].lower()
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴅᴀʟᴄs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴅᴀʟᴄs".format(coins)) 
  rnd = random.choice(['heads','tails'])
  if cmd not in possible:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ sʜᴏᴜʟᴅ ᴛʀʏ ʜᴇᴀᴅs ᴏʀ ᴇɪᴛʜᴇʀ ᴛᴀɪʟs.")
  if cmd in ['h','head','heads']:
      if rnd == 'heads':
          user_won = True         
      else:
          user_won = False
  if cmd in ['t','tail','tails']:
      if rnd == 'tails':
          user_won = True
      else:
          user_won = False
  BET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not user_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply_photo(photo=random.choice(photo), caption="🛑 ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {0}!\n• ʏᴏᴜ ʟᴏsᴛ `{1:,}` ᴄᴏɪɴs\n• ᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ : `{2:,}` ᴅᴀʟᴄs".format(rnd,to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply_photo(photo=random.choice(photo), caption="✅ ᴛʜᴇ ᴄᴏɪɴ ʟᴀɴᴅᴇᴅ ᴏɴ {0}!\nʏᴏᴜ ᴡᴏɴ `{1:,}` ᴄᴏɪɴs\nᴛᴏᴛᴀʟ ʙᴀʟᴀɴᴄᴇ : `{2:,}` ᴅᴀʟᴄs".format(rnd,to_bet,new_wallet)) 
     
# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("dart"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)
  if user.id not in DART_DICT.keys():
      DART_DICT[user.id] = None     
  if DART_DICT[user.id]:
      x= await can_play(DART_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴅᴀʀᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_photo(photo=random.choice(photo), caption="ᴏᴋ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴅᴀʟᴄs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴅᴀʟᴄs".format(coins))
  m = await client.send_dice(chat_id,'🎯')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  DART_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ `{0:,}` ᴅᴀʟᴄs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴅᴀʟᴄs".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ `{0:,}` ᴅᴀʟᴄs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}`ᴅᴀʟᴄs.".format(to_bet,new_wallet))
     
 # --------------------------------------------------------------------------------- #
     
@Hiroko.on_message(filters.command("bowl"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username) 
  if user.id not in BOWL_DICT.keys():
      BOWL_DICT[user.id] = None     
  if BOWL_DICT[user.id]:
      x= await can_play(BOWL_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴏᴡʟ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_photo(photo=random.choice(photo), caption="ᴏᴋ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴅᴀʟᴄs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴅᴀʟᴄs".format(coins))
  m = await client.send_dice(chat_id,'🎳')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BOWL_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("🛑 sᴀᴅ ᴛᴏ sᴀʏ! ʙᴜᴛ ʏᴏᴜ ʟᴏsᴛ `{0:,}` ᴅᴀʟᴄs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴅᴀʟᴄs".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ `{0:,}` ᴅᴀʟᴄs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴅᴀʟᴄs.".format(to_bet,new_wallet))
  
# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command("basket"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)  
  if user.id not in BASKET_DICT.keys():
      BASKET_DICT[user.id] = None     
  if BASKET_DICT[user.id]:
      x= await can_play(BASKET_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ʙᴀsᴋᴇᴛ ᴀɢᴀɪɴ ɪɴ ʟɪᴋᴇ `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_photo(photo=random.choice(photo), caption="ᴏᴋ! ʙᴜᴛ ʜᴏᴡ ᴍᴜᴄʜ ʏᴏᴜ ᴀʀᴇ ɢᴏɴɴᴀ ʙᴇᴛ.")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴡᴀɴɴᴀ ʙᴇᴛ 𝟶 ? ʟᴏʟ!") 
  elif to_bet > coins:
      return await message.reply_text(_["minigames4"].format(coins))
  m = await client.send_dice(chat_id,'🏀')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BASKET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴅᴀʟᴄs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴅᴀʟᴄs".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("✅ ᴡᴏᴡ! ʏᴏᴜ ᴡᴏɴ `{0:,}` ᴅᴀʟᴄs\n• ᴄᴜʀᴇᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ✑ `{1:,}` ᴅᴀʟᴄs.".format(to_bet,new_wallet))

# --------------------------------------------------------------------------------- #
                                                                                                      
@Hiroko.on_message(filters.command(["pay", "transfer"]) & filters.group)
async def _pay(client,message):
    if not message.reply_to_message:
        return await message.reply_photo(photo=random.choice(photo), caption="ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ")
    to_user =  message.reply_to_message.from_user
    from_user = message.from_user
    if to_user.id == from_user.id:
        if message.from_user.id not in SUPREME_USERS:
            return
    if not await is_player(to_user.id):
        await create_account(to_user.id,to_user.username)
    if not await is_player(from_user.id):
        await create_account(from_user.id,from_user.username)
    if len(message.command) < 2:
        return await message.reply_photo(photo=random.choice(photo), caption="ᴜsᴀɢᴇ : /pay `100`")
    amount = message.command[1]
    to_pay =  message.command[1].lower()
    tcoins = await user_wallet(to_user.id)
    fcoins = await user_wallet(from_user.id)
    if amount == '*':
        if message.from_user.id not in SUPREME_USERS:
            amount = fcoins
    elif not amount.isdigit():
       return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴛʜɪɴᴋs ᴛʜᴀᴛ ɪᴛ's ᴀ ᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ?")
    amount = int(amount)
    if amount == 0:
        return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴡᴀɴɴᴀ 𝟶 ʟᴏʟ!") 
    elif amount > fcoins:
        if message.from_user.id not in SUPREME_USERS:
            return await message.reply_photo(photo=random.choice(photo), caption="ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴀᴛ ᴍᴜᴄʜ ᴅᴀʟᴄs ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ ✑ `{0:,}` ᴅᴀʟᴄs".format(fcoins))
    if message.from_user.id not in SUPREME_USERS:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
        await gamesdb.update_one({'user_id' : from_user.id},{'$set' : {'coins' : fcoins - amount }})
    else:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
    await message.reply_photo(photo=random.choice(photo), caption="sᴜᴄᴄᴇss! {0} ᴘᴀɪᴅ {1:,} ᴅᴀʟᴄs ᴛᴏ {2}.".format(from_user.mention,amount,to_user.mention))

# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["top","leaderboard"]))
async def _top(client,message): 
    x = gamesdb.find().sort("coins", pymongo.DESCENDING)
    msg = "**📈 GLOBAL LEADERBOARD | 🌍**\n\n"
    counter = 1
    for i in await x.to_list(length=None):
        if counter == 11:
            break
        if i["coins"] == 0:
            pass
        else:
            user_name = i["username"]
            link = f"[{user_name}](https://t.me/{user_name})"
            if not user_name:
                user_name = i["user_id"]
                try:
                    link = (await Hiroko.get_users(user_name)).mention
                except Exception as e:
                    print(e)
                    link = user_name
            
            coins = i["coins"]
            if counter == 1:
               msg += f"{counter:02d}.**👑 {link}** ⪧ {coins:,}\n"
                
            else:
                msg += f"{counter:02d}.**👤 {link}** ⪧ {coins:,}\n"
            counter += 1
    await message.reply(msg,disable_web_page_preview=True)



# --------------------------------------------------------------------------------- #

@Hiroko.on_message(filters.command(["bal","balance","dalcs"]))
async def _bal(client,message):
    user = message.from_user
    if not await is_player(user.id):
        await create_account(user.id,message.from_user.username)
    coins = await user_wallet(user.id)
    await message.reply_photo(photo=random.choice(photo), caption="⁕ {0}'s ᴡᴀʟʟᴇᴛ.\n≪━─━─━─━─◈─━─━─━─━≫\n**Đ ⪧** `{1:,}` \n**≪━─━─━─━─◈─━─━─━─━≫".format(user.mention,coins))


 # --------------------------------------------------------------------------------- #
   
@Hiroko.on_message(filters.command("set dalcs"))
async def _bal(client,message):
    user = message.from_user
    if user.id not in SUPREME_USERS:
        return 
    if not message.reply_to_message:
        return await message.reply_photo(photo=random.choice(photo), caption="ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ")
    if not message.reply_to_message.from_user:
        return await message.reply_photo(photo=random.choice(photo), caption="ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ")
    from_user = message.reply_to_message.from_user
    if not await is_player(from_user.id):
        await create_account(from_user.id,from_user.username) 
    if len(message.command) < 2:
        return await message.reply_photo(photo=random.choice(photo), caption="ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟᴜᴇ ᴛᴏ sᴇᴛ ᴜsᴇʀs ᴅᴀʟᴄs")
    dalcs = message.command[1]
    if not dalcs.isdigit():
        return await message.reply_photo(photo=random.choice(photo), caption="ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴠᴀʟᴜᴇ ɪs ɴᴏᴛ ᴀ ɪɴᴛᴇɢᴇʀ.")
    dalcs = abs(int(dalcs))
    await gamesdb.update_one({'user_id' : from_user.id},{'$set' : {'coins' : dalcs }})
    return await message.reply_photo(photo=random.choice(photo), caption=f"sᴜᴄᴄᴇss ! sᴇᴛ ᴛʜᴇ ᴅᴀʟᴄs ᴏғ ᴜsᴇʀ {from_user.mention} ᴛᴏ {dalcs}")
    


      
