import datetime
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli



# --------------------------------------------------------------------------------- #


mongo = MongoCli(MONGO_URL)
db = mongo.Anonymous

gamesdb = db.games


# --------------------------------------------------------------------------------- #


async def create_account(user_id,user_name):
  dic = {
    "user_id" : user_id,
    "username" : user_name,
    "character" : char_name,
    "experience" : experience,
    "level" : level,
    "bank" : bank,
    "coins" : 500,
    
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


