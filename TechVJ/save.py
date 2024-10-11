# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
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

def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default


async def downstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Downloaded : {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# upload status
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










PROGRESS_BAR = """
╭─── ✪ Progress ✪
├ ⚡ [{0}]
├ 🚀 Speed: {3}/s
├ 📟 Completed: {1}/{2}
├ ⏳ Time: {4}
╰─── `[✪ Team SPY ✪](https://t.me/devggn)`
"""

def calculate_mbps(size_in_bytes, elapsed_time):
    """
    Convert the size from bytes to megabits per second (Mbps).
    :param size_in_bytes: Size transferred so far in bytes.
    :param elapsed_time: Time elapsed in seconds.
    :return: Speed in Mbps.
    """
    if elapsed_time == 0 or size_in_bytes == 0:
        return 0.0  # Prevent division by zero or invalid sizes
    size_in_megabits = (size_in_bytes * 8) / 1_000_000  # Convert bytes to megabits
    return size_in_megabits / elapsed_time

def format_time(seconds):
    """
    Convert time in seconds to a human-readable format of minutes and seconds.
    """
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}m {int(seconds)}s"

async def downstatus(client: Client, statusfile, message):
    """
    Monitor download status and update the Telegram message.
    """
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)  # Wait for status file to be created

    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Downloaded: {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

async def upstatus(client: Client, statusfile, message):
    """
    Monitor upload status and update the Telegram message.
    """
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)

    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Uploaded: {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

def progress(current, total, message=None, type='default', start_time=None, bar_length=25, display_in_terminal=True):
    """
    Display a custom progress bar with download/upload speed in Mbps, completed progress, and time.
    """
    if start_time is None:
        start_time = time.time()  # Default to current time if not provided

    # Check if 'current' and 'total' are valid
    if current <= 0 or total <= 0:
        print("Error: File size equals to 0 B", file=sys.stderr)
        return

    # Calculate progress percentage and elapsed time
    progress_percentage = current * 100 / total
    elapsed_time = time.time() - start_time

    # Calculate speed in Mbps
    mbps_speed = calculate_mbps(current, elapsed_time)

    # Format elapsed time
    formatted_time = format_time(elapsed_time)

    # Generate progress bar visualization
    filled_length = int(bar_length * current // total)
    bar_fill = "●" * filled_length
    bar_empty = "○" * (bar_length - filled_length)
    progress_bar = f"{bar_fill}{bar_empty}"

    # Display formatted progress bar with speed, completion, and time
    output = PROGRESS_BAR.format(progress_bar, current, total, f"{mbps_speed:.2f} Mbps", formatted_time)

    # Ensure the directory for the file exists
    file_id = message.id if message and hasattr(message, 'id') else 'progress'
    file_path = f'{file_id}{type}status.txt'

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write progress, speed, and ETA to the file
        with open(file_path, "w") as fileup:
            fileup.write(output)
    except IOError as e:
        print(f"Error writing progress to file: {e}", file=sys.stderr)

    # Optionally display the progress in the terminal
    if display_in_terminal:
        sys.stdout.write(f"\r{output}")
        sys.stdout.flush()

# Example usage
# start_time = time.time()
# progress(30 * 1024 * 1024, 100 * 1024 * 1024, message=None, type='upload', start_time=start_time, bar_length=30)




# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/kingvj01")
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_botz')
	]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(message.chat.id, f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\nFor downloading restricted content /login first.\n\nKnow how to use bot by - /help</b>", reply_markup=reply_markup, reply_to_message_id=message.id)
    return


# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(message.chat.id, f"{HELP_TXT}")

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
        for msgid in range(fromID, toID+1):
            # private
            if "https://t.me/c/" in message.text:
                user_data = database.find_one({'chat_id': message.chat.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                chatid = int("-100" + datas[4])
                await handle_private(client, acc, message, chatid, msgid)
    
            # bot
            elif "https://t.me/b/" in message.text:
                user_data = database.find_one({"chat_id": message.chat.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
	        # public
            else:
                username = datas[3]

                try:
                    msg = await client.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                    return
                try:
                    await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    try:    
                        user_data = database.find_one({"chat_id": message.chat.id})
                        if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                            await client.send_message(message.chat.id, strings['need_login'])
                            return
                        acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                        await acc.connect()
                        await handle_private(client, acc, message, username, msgid)
                        
                    except Exception as e:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # wait time
            await asyncio.sleep(3)


# handle private
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)
    chat = message.chat.id
    if "Text" == msg_type:
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            return

    smsg = await client.send_message(message.chat.id, 'Downloading', reply_to_message_id=message.id)
    dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message,"down"])
        os.remove(f'{message.id}downstatus.txt')
        
    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)  
    
    upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))

    if msg.caption:
        caption = msg.caption
    else:
        caption = None
            
    if "Document" == msg_type:
        try:
            ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_document(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        if ph_path != None: os.remove(ph_path)
        

    elif "Video" == msg_type:
        try:
            ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        if ph_path != None: os.remove(ph_path)

    elif "Animation" == msg_type:
        try:
            await client.send_animation(chat, file, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        

    elif "Sticker" == msg_type:
        try:
            await client.send_sticker(chat, file, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        

    elif "Voice" == msg_type:
        try:
            await client.send_voice(chat, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

    elif "Audio" == msg_type:
        try:
            ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            ph_path = None

        try:
            await client.send_audio(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        
        if ph_path != None: os.remove(ph_path)

    elif "Photo" == msg_type:
        try:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
    
    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
        os.remove(file)
    await client.delete_messages(message.chat.id,[smsg.id])


# get the type of message
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
        
