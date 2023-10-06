import os
from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_USERNAME = getenv("BOT_USERNAME", "HirokoRobot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "6632922889:AAELJEcs4yKDlcqEITwGDHju_rOKo5X_bA0")
OWNER_ID = int(getenv("OWNER_ID", "6280048819"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6280048819").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Hiroko:Hiroko@cluster0.1hztkgz.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQATqQrnrJwDN7OV7HpeayrvtHVULkQgNjBF7QRWNRHL4P-UcPuwU196xbb8jynABGmx7XUZZyQQtssulrd0IUtiJPCgN0mPyMd-mKg4BGlMEz-jRUkSOsHP1wEdnnUp3wxTjls6nEUNQCEtCH-z81zPEgC-xh1q4rjppfDXBdGdegEvzkI9iOoTmVP4nTmizeDXuhheZTqy6wizE8DQ4fWkiUoTFzgTXj9iVDmebdnVWqzIMqX5GDl718QtTu8vowi5vNwK0LTxXQmcbFvlyqaBgkZbs4LfOkjFo5Dmt9wiNg_8XIv5RFAGJ1k4KrEvcOrLzegYi4gzrGYHwMT-v-hmAAAAAWwKSlsA")
