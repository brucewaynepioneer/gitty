# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
import os
import logging
import asyncio 
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
import time
import os
import threading
import json
import re  # Imported for regex handling
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

def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

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
            if "https://t.me/c/" in message.text:
                user_data = database.find_one({'chat_id': message.chat.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                chatid = int("-100" + datas[4])
                await handle_private(client, acc, message, chatid, msgid)
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
            await asyncio.sleep(3)



MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB in bytes

# Configure logging
logging.basicConfig(filename='bot_uploads.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    try:
        msg: Message = await acc.get_messages(chatid, msgid)
        msg_type = get_message_type(msg)
        chat = message.chat.id

        if "Text" == msg_type:
            try:
                await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id)
            except Exception as e:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
                logging.error(f"Failed to send text message: {e}")
                return

        smsg = await client.send_message(message.chat.id, 'Downloading', reply_to_message_id=message.id)
        dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))

        try:
            file = await acc.download_media(msg, progress=progress, progress_args=[message, "down"])
            os.remove(f'{message.id}downstatus.txt')
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            logging.error(f"Failed to download media: {e}")
            return

        upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))

        if msg.caption:
            caption = msg.caption
        else:
            caption = None

        # Check if the file size exceeds the 2GB limit
        if os.path.getsize(file) > MAX_FILE_SIZE:
            await split_and_upload(client, message, file, msg_type, caption)
        else:
            await upload_file(client, message, file, msg_type, caption)

        if os.path.exists(f'{message.id}upstatus.txt'):
            os.remove(f'{message.id}upstatus.txt')
        os.remove(file)
        await client.delete_messages(message.chat.id, [smsg.id])
    except Exception as e:
        logging.error(f"Failed to handle private message: {e}")
        await client.send_message(message.chat.id, f"Error handling request: {e}", reply_to_message_id=message.id)

async def upload_file(client, message, file, msg_type, caption):
    chat = message.chat.id
    try:
        if "Document" == msg_type:
            await client.send_document(chat, file, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        elif "Video" == msg_type:
            await client.send_video(chat, file, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        elif "Photo" == msg_type:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id)
        elif "Animation" == msg_type:
            await client.send_animation(chat, file, reply_to_message_id=message.id)
        elif "Audio" == msg_type:
            await client.send_audio(chat, file, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        logging.info(f"Successfully uploaded {msg_type} file: {file}")
    except Exception as e:
        await client.send_message(chat, f"Error uploading file: {e}", reply_to_message_id=message.id)
        logging.error(f"Failed to upload {msg_type} file: {e}")

async def split_and_upload(client, message, file_path, msg_type, caption):
    """
    Splits a file into parts if its size exceeds 2GB and uploads each part separately.
    """
    file_size = os.path.getsize(file_path)
    part_number = 1
    chat = message.chat.id

    try:
        with open(file_path, 'rb') as f:
            while file_size > 0:
                part_file_name = f"{file_path}.part{part_number}"
                with open(part_file_name, 'wb') as part_file:
                    chunk_size = min(MAX_FILE_SIZE, file_size)
                    part_file.write(f.read(chunk_size))

                # Upload the part
                try:
                    if "Document" == msg_type:
                        await client.send_document(chat, part_file_name, caption=f"{caption} - Part {part_number}", reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
                    elif "Video" == msg_type:
                        await client.send_video(chat, part_file_name, caption=f"{caption} - Part {part_number}", reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
                    elif "Audio" == msg_type:
                        await client.send_audio(chat, part_file_name, caption=f"{caption} - Part {part_number}", reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
                    logging.info(f"Successfully uploaded {msg_type} part {part_number}: {part_file_name}")
                except Exception as e:
                    await client.send_message(chat, f"Error uploading part {part_number}: {e}", reply_to_message_id=message.id)
                    logging.error(f"Failed to upload part {part_number} of {msg_type}: {e}")
                    return

                # Delete the part after uploading
                os.remove(part_file_name)

                # Move to the next part
                file_size -= chunk_size
                part_number += 1
    except Exception as e:
        await client.send_message(chat, f"Error splitting file: {e}", reply_to_message_id=message.id)
        logging.error(f"Failed to split and upload file: {e}")

# The new /replace command
@Client.on_message(filters.command("replace") & filters.text)
async def handle_replace(client: Client, message: Message):
    user_id = message.from_user.id

    # Updated regex to handle any number of word replacements
    match = re.match(r'/replace\s+((?:\"[^\"]+\"\s*)+)\s*->\s+((?:\"[^\"]+\"\s*)+)', message.text, re.UNICODE)
    if match:
        old_words = re.findall(r'"([^"]+)"', match.group(1))
        new_words = re.findall(r'"([^"]+)"', match.group(2))

        if len(old_words) != len(new_words):
            return await client.send_message(message.chat.id, "The number of words/phrases to replace must match the number of new words/phrases.", reply_to_message_id=message.id)

        delete_words = load_delete_words(user_id)
        if any(old_word in delete_words for old_word in old_words):
            return await client.send_message(message.chat.id, "One or more words in the old words list are in the delete set and cannot be replaced.", reply_to_message_id=message.id)

        replacements = dict(zip(old_words, new_words))
        save_replacement_words(user_id, replacements)

        replacement_summary = ', '.join([f"'{old}' -> '{new}'" for old, new in replacements.items()])
        return await client.send_message(message.chat.id, f"Replacements saved: {replacement_summary}", reply_to_message_id=message.id)
    
    # Regex for single word replacement
    match_single = re.match(r'/replace\s+"([^"]+)"\s*->\s*"([^"]+)"', message.text, re.UNICODE)
    if match_single:
        old_word, new_word = match_single.groups()
        delete_words = load_delete_words(user_id)

        if old_word in delete_words:
            return await client.send_message(message.chat.id, f"The word '{old_word}' is in the delete set and cannot be replaced.", reply_to_message_id=message.id)

        replacements = {old_word: new_word}
        save_replacement_words(user_id, replacements)

        return await client.send_message(message.chat.id, f"Replacement saved: '{old_word}' will be replaced with '{new_word}'", reply_to_message_id=message.id)
    
    return await client.send_message(message.chat.id, "Usage:\nFor single word replacement: /replace \"WORD\" -> \"REPLACEWORD\"\nFor multiple word replacements: /replace \"WORD1\" \"WORD2\" ... -> \"NEWWORD1\" \"NEWWORD2\" ...", reply_to_message_id=message.id)
