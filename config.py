import os
from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_USERNAME = getenv("BOT_USERNAME", "HirokoRobot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "6632922889:AAELJEcs4yKDlcqEITwGDHju_rOKo5X_bA0")
OWNER_ID = int(getenv("OWNER_ID", "6280048819"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6280048819 6149191605").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Hiroko:Hiroko@cluster0.1hztkgz.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQGZtJEAIAj1p1iTIYgtn5wIUtTZqMPyOTYXCEviItTdDf0DQXFgrNsS-v0Pp5wpj7zSIgsc6BfV4KkX_Xt9f6rlounnlja0HmNuzBbizmph6Fo_FLrDv-wxqRwDMGSDltvKJzHoQiQHmlvEy0b5VNh94ZuebcIddUOGdHAxyEqV4UIeUZm2qZrHUbtLGo763PPruoXHKFjcVwHuQp4Zc3OgOmiJOnH5lwC2O0Mtt0GESRrfLvf8EjWGd42WgHGnMq_v55QdB4shURee2LDqboMaxSPLm20M1wZOKI2w0NU3cI-Wo7xUl5WgFu96BYdiI1_Hdd8uBRTXzX2GlMb7mhwa3UngAAAAFsCkpbAA")
