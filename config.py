# THIS CODE FULLY MODIFIED BY @Mobarak46. NOW THIS BOT CAN RUN IN RENDER

import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ────────────────────── TELEGRAM API ──────────────────────
API_ID = 22175614
API_HASH = "5dab14fb645d7c6b5f8d094581192e04"

# ────────────────────── BOT TOKEN ─────────────────────────
BOT_TOKEN = "8121823141:AAE7nHSJuxNMySY3SmtpJ5hFrO_X4RpbPpo"

# ────────────────────── DATABASE ──────────────────────────
MONGO_DB_URI = "mongodb+srv://121manokaran:RrQU9aVnFnEwonSX@cluster0.uxizm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ────────────────────── BASIC SETTINGS ────────────────────
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 60))

LOG_GROUP_ID = -1001654008278 #Enter Channel id... Don't enter Group id if done you will get error 
OWNER_ID = 1491400016

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
STRING1 = "AQH-pWEAdpaX9RNqogQdjH2lHvYJ3nk4bldabDXDs4CAb7CxZ0apKRRykSeqtdJ_BEQN9rE7sBRddyJ07FUJGi2xqRIp6pU2UHAwa7gkRW1674Gd-emSNECHyPcWVyzgzvvJm1t3nJ_OEJIZf4q3C_0daxYZypOO7ZROhZn48FSnfkT0BOHDxHcVxYObjk8nRj8q2qsu3dF2Uw_59iQsSu4OCg1cRlVQSiUeCs6U1HW1MPEATUK3casd9_YNDRYM0049etmT6i0VHkQgKD47BIj2fbhMCDscuke70ix3Bj1W_GkJXCU55WgHJGrjbRBdl45LXxw-iPqUEczpOALZD8WqTjby6gAAAAH9Kh65AA"
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
START_IMG_URL = "https://i.ibb.co/m50CQT28/x.jpg"
PING_IMG_URL = "https://graph.org/file/f586172fe40a0b5d0b0df.jpg"
PLAYLIST_IMG_URL = "https://graph.org/file/763a841a2ad5cbb1e2fc5.jpg"
STATS_IMG_URL = "https://graph.org/file/f586172fe40a0b5d0b0df.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
TELEGRAM_VIDEO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"

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







