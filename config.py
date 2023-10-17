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
SESSION_STRING = getenv("SESSION_STRING", "AQCjwmEALYm9fGAVnxx7u_LLfuNq9bvhTv26tOjgB_mXe7XL-5SaKo6qH87uvSXg5HnwyUVUpAAvepYSfr5zZvUEbthiiPpka3SkzI6LNG_8wwfadUegoWCQDSlj9ykbDVQUclLuONp9gYQbjEk6is6WVq5q1NYUDMPX5jQeFp6LrqMeLRw7pxwSl0o9P6jW2ilbQcuN5A76uwSLcjurevqvZvt3Fc_87xtMrXbi0dDseWJvJlmrXwNtMxr8m9NFNAbJ1BlnGnWx6cUyAmcpT5PG8N6BYRLyA0W4bvp8Lx1xNV-tRcN7XERWPw72-O5TBuXzuuNV-zPN5GNtilUh_4Hm1pdRZwAAAAGBS9ZQAA")
