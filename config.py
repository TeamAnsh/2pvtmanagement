import os
from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_USERNAME = getenv("BOT_USERNAME", "HirokoRobot")
COMMAND_HANDLER = ["/", "!"]
BOT_TOKEN = getenv("BOT_TOKEN", "6632922889:AAELJEcs4yKDlcqEITwGDHju_rOKo5X_bA0")
OWNER_ID = int(getenv("OWNER_ID", "6280048819"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6280048819 6149191605 5030730429").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Hiroko:Hiroko@cluster0.1hztkgz.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQDF58RfZJXfD5MFpNMpPIeVlILetFdo9PZJfOecPDCSzO8qojK48m4zWkCsR9HgdFS747U9ldqknGzsmaAUzZ74RLKJoyjR-8xE8KPFfFz5pd7VGOEkW23rygo2UQmOBg4ZeDPSdfurWWcAPxImaOp6ZTMlV-LG6CjW4xH1Nh6TDmprlLaEMCh-jATUm0xDSmrianZahP33WQSKn5Cinqf6a-1zDAJDjGNQAWtmn1hZsA7n-3mlN9HcE2v2uyl6Xbodtms72hVERvH4pRKqiVCL2Rc68L-4cHJ32-Im31d42RvIjdiJGQ0dgtXzScH0AQv8-2CK-xH208KpGssOgR49AAAAAWwKSlsA")
