import asyncio
import aiohttp
import re
from typing import Union
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from alicex.utils.formatters import time_to_seconds

# --- CONFIGURATION ---
# Your API Key and URL
API_URL = "http://213.199.39.92:1470"
API_KEY = "1a873582a7c83342f961xx0a177b2b26" 

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def _api_request(self, query: str, video: bool = False):
        """Helper to call your custom API"""
        async with aiohttp.ClientSession() as session:
            try:
                # Call the /youtube endpoint
                url = f"{API_URL}/youtube"
                params = {
                    "query": query,
                    "video": "true" if video else "false",
                    "api_key": API_KEY
                }
                async with session.get(url, params=params, timeout=30) as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    if "error" in data:
                        return None
                    return data
            except:
                return None

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        
        # Call API
        data = await self._api_request(link)
        
        if not data:
            return None, 0, 0, None, None

        title = data.get("title")
        duration_str = str(data.get("duration", 0)) # API returns seconds usually
        
        # Convert duration logic
        try:
            dur_sec = int(float(duration_str))
            duration_min = f"{dur_sec // 60}:{dur_sec % 60:02d}"
        except:
            dur_sec = 0
            duration_min = "00:00"

        thumbnail = data.get("thumbnail")
        vidid = data.get("id")
        
        return title, duration_min, dur_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        data = await self._api_request(link)
        return data.get("title") if data else None

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        data = await self._api_request(link)
        return data.get("duration") if data else None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        data = await self._api_request(link)
        return data.get("thumbnail") if data else None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
            
        # Call API specifically asking for Video stream
        data = await self._api_request(link, video=True)
        
        if data and data.get("stream_url"):
            # Return 1 (Success) and the API Stream Link
            return 1, data["stream_url"]
        
        return 0, "Failed to get stream from API"

    async def track(self, link: str, videoid: Union[bool, str] = None):
        # API handles search automatically if 'link' is a query
        data = await self._api_request(link)
        
        if not data:
            return None, None

        title = data.get("title")
        vidid = data.get("id")
        yturl = f"https://www.youtube.com/watch?v={vidid}"
        duration = data.get("duration")
        thumbnail = data.get("thumbnail")

        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration, 
            "thumb": thumbnail,
        }
        return track_details, vidid

    # --- LEGACY METHODS (Kept to prevent bot crashing if called) ---
    # Since the API handles everything, these complex local downloaders 
    # are technically not needed for streaming, but if your bot uses them
    # for specific file sending features, we can keep simple wrappers.

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        # For Music Bot Streaming: The 'video()' function above returns the stream link.
        # This 'download' function is usually for saving files to disk.
        
        # If the bot is asking for a direct stream link (common in Music Bots):
        if video: 
             _, stream_url = await self.video(link, videoid)
             return stream_url, True # True means it's a direct link, not a file path

        # If the bot ACTUALLY needs a file download (e.g. /song command),
        # we can just return the stream URL from the API, 
        # because the API link acts like a file download!
        
        is_video = bool(songvideo or video)
        data = await self._api_request(link, video=is_video)
        
        if data and data.get("stream_url"):
            # API Link acts as the file path
            return data["stream_url"], True 
            
        return None, None
