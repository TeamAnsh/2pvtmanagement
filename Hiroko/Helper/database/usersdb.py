from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient


mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.users



async def get_served_users():
    user_list = []
    async for user in db.users.find({"user": {"$gt": 0}}):
        user_list.append(user['user'])
    return user_list

async def is_served_user(user):
    users = await get_served_users()
    if user in users:
        return True
    else:
        return False

async def add_served_user(user):
    users = await get_served_users()
    if user in users:
        return
    else:
        await db.users.insert_one({"user": user})

async def remove_served_user(user):
    users = await get_served_users()
    if not user in users:
        return
    else:
        await db.users.delete_one({"user": user})


