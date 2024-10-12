import sys
import time
import asyncio 
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
import time
import os
import threading
import json
from config import API_ID, API_HASH
from database.db import database 
from TechVJ.strings import strings, HELP_TXT



PROGRESS_BAR = """
╭─── ✪ Progress ✪
├ ⚡ [{0}]
├ 🚀 Speed: {3}/s
├ 📟 Completed: {1}/{2}
├ ⏳ Time: {4}
╰─── `[✪ Team SPY ✪](https://t.me/devggn)`
"""

# Generate a formatted progress bar string
def generate_progress_bar(current, total, start_time):
    progress = int((current / total) * 10)
    bar = '●' * progress + '○' * (10 - progress)
    
    completed = f"{current}B"
    total_size = f"{total}B"
    
    elapsed_time = time.time() - start_time
    speed = f"{current / elapsed_time:.2f}B"  # Speed in bytes per second
    
    if current > 0:
        estimated_time = (total - current) / (current / elapsed_time)
    else:
        estimated_time = 0
    
    time_remaining = time.strftime("%H:%M:%S", time.gmtime(estimated_time))
    
    return PROGRESS_BAR.format(bar, completed, total_size, speed, time_remaining)

# Progress writer
def progress(current, total, message, type, start_time):
    progress_bar = generate_progress_bar(current, total, start_time)
    
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")
    
    # Update the message with the progress bar
    asyncio.create_task(update_progress_message(message, progress_bar))

# Async function to update the message with the progress bar
async def update_progress_message(message, progress_bar):
    try:
        await message.edit_text(progress_bar)
    except Exception as e:
        print(f"Error updating progress: {e}")

# Upload status
async def upstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
    
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Uploaded : {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

# Handle private messages
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)
    chat = message.chat.id
    start_time = time.time()  # Start time for the progress calculation
    
    smsg = await client.send_message(message.chat.id, 'Downloading', reply_to_message_id=message.id)
    dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))
    
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message, "down", start_time])
        os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
    
    upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))

    # Other media handling code as in your original code...
    # (Document, Video, Audio, etc.)

# Get message type
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass

# Other functions such as start, help, and save would remain the same...
