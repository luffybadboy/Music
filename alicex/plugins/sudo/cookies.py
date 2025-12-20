import os
import asyncio
from pyrogram import filters
from alicex import app
from alicex.misc import SUDOERS
from alicex.utils.decorators.language import language

# Directory to store cookies
COOKIES_DIR = "cookies/"

# Ensure directory exists
if not os.path.exists(COOKIES_DIR):
    os.makedirs(COOKIES_DIR)

@app.on_message(filters.command(["addcookie", "uploadcookie"]) & SUDOERS)
@language
async def add_cookie_plugin(client, message, _):
    """
    Uploads a cookie file attached to the message.
    """
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text("<b>Example:</b> Reply to a <code>.txt</code> cookie file with <code>/addcookie</code>.")
    
    doc = message.reply_to_message.document
    if not doc.file_name.endswith(".txt"):
        return await message.reply_text("❌ Please upload a valid <code>.txt</code> file (Netscape format).")

    # Generate a unique filename to avoid overwriting
    existing_files = os.listdir(COOKIES_DIR)
    count = len([f for f in existing_files if f.startswith("cookie_") and f.endswith(".txt")]) + 1
    new_filename = f"cookie_{count}.txt"
    file_path = os.path.join(COOKIES_DIR, new_filename)

    status = await message.reply_text("⬇️ Downloading cookie file...")
    
    try:
        await message.reply_to_message.download(file_name=file_path)
        await status.edit_text(f"<b>✅ Cookie Added Successfully!</b>\n\n<b>📁 Saved as:</b> <code>{new_filename}</code>\n<b>📂 Location:</b> <code>{COOKIES_DIR}</code>")
    except Exception as e:
        await status.edit_text(f"❌ Failed to save cookie.\n\nError: <code>{str(e)}</code>")


@app.on_message(filters.command(["rmcookie", "delcookie"]) & SUDOERS)
@language
async def remove_cookie_plugin(client, message, _):
    """
    Deletes a specific cookie file.
    """
    if len(message.command) < 2:
        return await message.reply_text("<b>Usage:</b> <code>/rmcookie [filename]</code>\n\nExample: <code>/rmcookie cookie_1.txt</code>")

    file_name = message.command[1]
    file_path = os.path.join(COOKIES_DIR, file_name)

    if not os.path.exists(file_path):
        return await message.reply_text(f"❌ File <code>{file_name}</code> not found in <code>{COOKIES_DIR}</code>.")

    try:
        os.remove(file_path)
        await message.reply_text(f"<b>🗑️ Deleted:</b> <code>{file_name}</code>")
    except Exception as e:
        await message.reply_text(f"❌ Error deleting file: <code>{str(e)}</code>")


@app.on_message(filters.command(["cookies", "listcookies"]) & SUDOERS)
@language
async def list_cookies_plugin(client, message, _):
    """
    Lists all available cookie files.
    """
    files = [f for f in os.listdir(COOKIES_DIR) if f.endswith(".txt")]
    
    if not files:
        return await message.reply_text("<b>📂 Cookie Directory is Empty!</b>\n\nUpload some using <code>/addcookie</code>.")

    file_list = "\n".join([f"• <code>{f}</code>" for f in files])
    count = len(files)
    
    await message.reply_text(f"<b>🍪 Available Cookies ({count}):</b>\n\n{file_list}")


@app.on_message(filters.command(["checkcookies", "cleancookies"]) & SUDOERS)
@language
async def check_cookies_plugin(client, message, _):
    """
    Checks all cookies, deletes dead ones, and reports status.
    """
    files = [f for f in os.listdir(COOKIES_DIR) if f.endswith(".txt")]
    
    if not files:
        return await message.reply_text("❌ No cookies found to check.")

    status_msg = await message.reply_text(f"<b>🔄 Checking {len(files)} cookies...</b>\nThis may take a moment.")
    
    working = 0
    dead = 0
    removed_files = []

    # A generic video URL to test connectivity (Short videos are faster to check)
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 

    for file_name in files:
        file_path = os.path.join(COOKIES_DIR, file_name)
        
        # We run a quick yt-dlp command to see if it can fetch metadata (-g) without error
        # --get-url (-g) is fast and doesn't download video
        cmd = f"yt-dlp --cookies {file_path} -g {test_url}"
        
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        # If return code is 0 (Success) and we got output, it's working
        if proc.returncode == 0 and stdout:
            working += 1
        else:
            # If it failed, we assume the cookie is dead/banned
            dead += 1
            removed_files.append(file_name)
            try:
                os.remove(file_path)
            except:
                pass

    # Create summary report
    report = (
        f"<b>📝 Cookie Health Check Report</b>\n\n"
        f"<b>✅ Working:</b> {working}\n"
        f"<b>❌ Dead & Removed:</b> {dead}\n"
    )

    if removed_files:
        report += f"\n<b>🗑️ Removed Files:</b>\n" + "\n".join([f"• <code>{f}</code>" for f in removed_files])
    else:
        report += "\n✨ All cookies are healthy!"

    await status_msg.edit_text(report)
