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
SESSION_STRING = getenv("SESSION_STRING", "BQGZtJEAs40N-RwHzX33L9wDBM4mp4BGoYevz0oZymRckipt54NYAfzI0NfM0MQlO1TmLmyRJcvrAw7ODez0zKVWw66m2vNaPReuekMSI1YNGblLKc4eYYhor_fpO7c3F92OK315hNZ_d4n53zNNUagOiPpeo1_5r6ZWL4OE8jkaxIrcGlQBwNUduy32NJoGSX5x7IC3CTafEYSEnn3jpud5uor1rAiI7mIgV0TB8vWogZLiZ7K4FeNJz_NgQesNpvTk8EbkL86611xi1w5kPHXCFMMInL077QpokawPy6oRmp_EYa3gkXba6dodxt51JPJ5imYX4xGSAYwPZx5I_DRfx7CpnQAAAAFsCkpbAA")
