import asyncio
import os
import re
import json
from typing import Union
import random
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from alicex.utils.database import is_on_off
# FIX: Added seconds_to_min here
from alicex.utils.formatters import time_to_seconds, seconds_to_min

# --- CONFIGURATION START ---
cookies_dir = "cookies/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
]
# --- CONFIGURATION END ---

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if out:
        return out.decode("utf-8")
    if errorz:
        return errorz.decode("utf-8")
    return out.decode("utf-8")

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def _get_random_cookie(self):
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)
        all_files = os.listdir(cookies_dir)
        txt_files = [os.path.join(cookies_dir, file) for file in all_files if file.endswith(".txt")]
        if not txt_files:
            return None 
        return random.choice(txt_files)

    def _get_random_agent(self):
        return random.choice(USER_AGENTS)

    async def _safe_sleep(self):
        await asyncio.sleep(random.uniform(0.5, 2.0))

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

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
        if "&" in link:
            link = link.split("&")[0]
        return await self.track(link)

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()
        
        if not re.search(self.regex, link):
            cmd_link = f"ytsearch1:{link}"
        else:
            cmd_link = link

        cmd_args = [
            "yt-dlp",
            "--dump-json",
            "--user-agent", current_agent,
            "--geo-bypass",
            "--no-check-certificate",
            "--quiet",
            "--no-playlist",
            cmd_link,
        ]

        if current_cookie:
            cmd_args.insert(1, "--cookies")
            cmd_args.insert(2, current_cookie)

        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        if stdout:
            info = json.loads(stdout.decode())
            if isinstance(info, list): 
                info = info[0] if info else {}
            
            title = info.get("title", "Unknown Title")
            duration_sec = info.get("duration", 0)
            duration_min = seconds_to_min(duration_sec)
            vidid = info.get("id")
            yturl = f"https://www.youtube.com/watch?v={vidid}"
            thumbnail = info.get("thumbnail", "https://telegra.ph/file/1e3b6d034293f7739943f.jpg")
            
            track_details = {
                "title": title,
                "link": yturl,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail,
            }
            return track_details, vidid
        else:
            raise Exception(f"yt-dlp failed: {stderr.decode()}")

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()
        
        cmd_args = [
            "yt-dlp",
            "--dump-json",
            "--user-agent", current_agent,
            "--flat-playlist",
            f"ytsearch10:{link}",
        ]

        if current_cookie:
            cmd_args.insert(1, "--cookies")
            cmd_args.insert(2, current_cookie)

        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        if stdout:
            results = [json.loads(line) for line in stdout.decode().splitlines() if line]
            if not results or query_type >= len(results):
                raise Exception("No results found")

            result = results[query_type]
            title = result.get("title")
            duration_sec = result.get("duration", 0)
            duration_min = seconds_to_min(duration_sec)
            vidid = result.get("id")
            thumbnail = f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg"
            
            return title, duration_min, thumbnail, vidid
        else:
             raise Exception(f"yt-dlp slider failed: {stderr.decode()}")

    async def title(self, link: str, videoid: Union[bool, str] = None):
        details, _ = await self.track(link, videoid)
        return details["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        details, _ = await self.track(link, videoid)
        return details["duration_min"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        details, _ = await self.track(link, videoid)
        return details["thumb"]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()
        
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        cmd_args = [
            "yt-dlp",
            "--user-agent", current_agent,
            "-g",
            "-f", "best[height<=?720][width<=?1280]",
            f"{link}",
        ]
        
        if current_cookie:
            cmd_args.insert(1, "--cookies")
            cmd_args.insert(2, current_cookie)

        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()

        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        
        cookie_cmd = f"--cookies {current_cookie}" if current_cookie else ""
        
        playlist = await shell_cmd(
            f"yt-dlp {cookie_cmd} --user-agent \"{current_agent}\" -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = playlist.split("\n")
            for key in result:
                if key == "":
                    result.remove(key)
        except:
            result = []
        return result

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()

        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        ytdl_opts = {
            "quiet": True, 
            "user_agent": current_agent
        }
        if current_cookie:
            ytdl_opts["cookiefile"] = current_cookie
        
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

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
        
        current_cookie = self._get_random_cookie()
        current_agent = self._get_random_agent()
        
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "user_agent": current_agent,
                "sleep_interval": 2,
            }
            if current_cookie:
                ydl_optssx["cookiefile"] = current_cookie

            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "user_agent": current_agent,
                "sleep_interval": 2,
            }
            if current_cookie:
                ydl_optssx["cookiefile"] = current_cookie

            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
                "user_agent": current_agent,
                "sleep_interval": 2,
            }
            if current_cookie:
                ydl_optssx["cookiefile"] = current_cookie

            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "user_agent": current_agent,
                "sleep_interval": 2,
            }
            if current_cookie:
                ydl_optssx["cookiefile"] = current_cookie

            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                cmd_args = [
                    "yt-dlp",
                    "--user-agent", current_agent,
                    "-g",
                    "-f", "best[height<=?720][width<=?1280]",
                    f"{link}",
                ]
                if current_cookie:
                    cmd_args.insert(1, "--cookies")
                    cmd_args.insert(2, current_cookie)

                proc = await asyncio.create_subprocess_exec(
                    *cmd_args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = None
                else:
                    return
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
