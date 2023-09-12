import asyncio
import logging
import time
from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from importlib import import_module
from os import environ, getenv, listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import config

loop = asyncio.get_event_loop()
load_dotenv()
boot = time.time()


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)



Hiroko = Client(
    ":Hiroko:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=config.BOT_TOKEN,
)


async_mongo_client = async_mongo(config.MONGO_URL)
db = async_mongo_client.hiroko



async def Hiroko_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await Hiroko.start()
    getme = await Hiroko.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(Hiroko_bot())


