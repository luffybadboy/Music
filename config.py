# THIS CODE FULLY MODIFIED BY @Mobarak46. NOW THIS BOT CAN RUN IN RENDER

import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ────────────────────── TELEGRAM API ──────────────────────
API_ID = 12345678
API_HASH = "abcdefghijklmnopqrstuvwxyz12345678910"

# ────────────────────── BOT TOKEN ─────────────────────────
BOT_TOKEN = "981298395:BBOOTTOOKKEENN"

# ────────────────────── DATABASE ──────────────────────────
MONGO_DB_URI = "mongodb+srv://1Mediagroup:ithinkthanoswasright@cluster0.nvidia.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ────────────────────── BASIC SETTINGS ────────────────────
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))

LOG_GROUP_ID = -1001657008278 #Enter Channel id... Don't enter Group id if done you will get error 
OWNER_ID = 12345678

# ────────────────────── HEROKU (DISABLED) ─────────────────
HEROKU_APP_NAME = None
HEROKU_API_KEY = None

UPSTREAM_REPO = None
UPSTREAM_BRANCH = None
GIT_TOKEN = None

# ────────────────────── SUPPORT LINKS ─────────────────────
SUPPORT_CHANNEL = "https://t.me/MUBIBOTz"
SUPPORT_GROUP = "https://t.me/Mobarak46"

# ────────────────────── ASSISTANT SETTINGS ────────────────
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# ────────────────────── SPOTIFY (OPTIONAL) ────────────────
SPOTIFY_CLIENT_ID = None
SPOTIFY_CLIENT_SECRET = None

# ────────────────────── PLAYLIST LIMIT ────────────────────
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# ────────────────────── FILE SIZE LIMITS ──────────────────
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

# ────────────────────── PYROGRAM SESSIONS ─────────────────
STRING1 = "AQH-pWEAdpaX9RNqogQdjH2lHvYJ3nk4bldabDXDs4CAb7CxZ0apKRRykSeqtdJ_BEQN9rE7sBRddyJ07FUJGi2xqRIp6pU2UHAwa7gkRW167"
STRING2 = None
STRING3 = None
STRING4 = None
STRING5 = None

# ────────────────────── BOT DATA ──────────────────────────
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ────────────────────── IMAGES ────────────────────────────
START_IMG_URL = ""
PING_IMG_URL = ""
PLAYLIST_IMG_URL = ""
STATS_IMG_URL = ""
TELEGRAM_AUDIO_URL = ""
TELEGRAM_VIDEO_URL = ""
STREAM_IMG_URL = ""
SOUNCLOUD_IMG_URL = ""
YOUTUBE_IMG_URL = ""
SPOTIFY_ARTIST_IMG_URL = ""
SPOTIFY_ALBUM_IMG_URL = ""
SPOTIFY_PLAYLIST_IMG_URL = ""

# ────────────────────── FUNCTIONS ─────────────────────────
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ────────────────────── VALIDATIONS ───────────────────────
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - SUPPORT_CHANNEL must start with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - SUPPORT_GROUP must start with https://"
)









