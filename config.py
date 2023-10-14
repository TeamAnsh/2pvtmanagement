import os
from os import getenv


API_ID = int(getenv("API_ID", "10732129"))
API_HASH = getenv("API_HASH", "ff00f45b106ccc2a69f1e74d1855e21e")
BOT_USERNAME = getenv("BOT_USERNAME", "TGxManagementbot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "6359973272:AAHvzBERjQ80oVfCSt6kdWZC3jWStBJcHy4")
OWNER_ID = int(getenv("OWNER_ID", "1674370115"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6280048819").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Ansh:Ansh@ansh.yptyojy.mongodb.net/Ansh?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "1AZWarzcBuxA6iXxLjilCucCx1diwaL1aXYdwn_CfFYap9vAo0PxFx2AquZkkkhHm6-LCqQ-I4m7rKpmDTgozFlB75M7IfZR1YhoOa_krmrzz0RFy5YUoSWRyLAZZTntOe9xrDb1VBYuve4S4GnRkCxZdYEVftvEZOUWnutI24dixZ2s_9G1NnFZyUEy3ETLrfFeeWtgGhptkDurfGrECKWkH1SjLOQpn8L4kOAgc0nUcBjOKFzyfzT7Q6VUnNZPb7Vi2q3blaZfDiA3vEWbiVgYetaXZiGAImE-MyNnRyOPQqShIc2laMUGDXxriEQBiJUz9gxDBJ7IyKKyOuuDC6u1j8wSNX4Y=")
