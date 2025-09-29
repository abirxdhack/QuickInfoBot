from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX
from utils.helpers import *

@bot.on_message(filters.command(["info", "id"], prefixes=COMMAND_PREFIX.split("|")))
async def info_command(bot: Client, message):
    LOGGER.info(f"Info command received from user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Info...`")
    command_parts = message.text.split()
    if len(command_parts) == 1 or (len(command_parts) > 1 and command_parts[1].lower() == 'me'):
        try:
            user = message.from_user
            response, full_name = format_user_response(user)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=full_name, copy_text=str(user.id))]]
            )
            try:
                photo_file_id, is_animated = await get_profile_photo_file_id(bot, user.id)
                if photo_file_id:
                    if is_animated:
                        await loading_message.edit_media(
                            media=InputMediaAnimation(
                                media=photo_file_id,
                                caption=response
                            ),
                            reply_markup=buttons
                        )
                    else:
                        await loading_message.edit_media(
                            media=InputMediaPhoto(
                                media=photo_file_id,
                                caption=response
                            ),
                            reply_markup=buttons
                        )
                    LOGGER.info(f"Sent user info with photo for user {user.id}")
                else:
                    await loading_message.edit_text(response, reply_markup=buttons)
                    LOGGER.info(f"Sent user info without photo for user {user.id}")
            except Exception as e:
                LOGGER.error(f"Error sending user info with photo for user {user.id}: {e}")
                await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
        except Exception as e:
            LOGGER.error(f"Error processing info command for user {message.from_user.id}: {e}")
            await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
    elif len(command_parts) > 1 and command_parts[1].lower() != 'me':
        LOGGER.info("Extracting username from the command")
        username = command_parts[1].strip('@').replace('https://', '').replace('http://', '').replace('t.me/', '').replace('/', '').replace(':', '')
        try:
            LOGGER.info(f"Fetching info for user or bot: {username}")
            chat = await bot.get_chat(username)
            entity_id = chat.id
            chat_type = chat.type
            is_group_context = chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]
            if chat_type in [ChatType.PRIVATE, ChatType.BOT]:
                entity = await bot.get_users(entity_id)
                response, full_name = format_user_response(entity, is_group_context, chat if is_group_context else None)
            else:
                entity = chat
                response, full_name = format_chat_response(chat)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=full_name, copy_text=str(entity_id))]]
            )
            try:
                photo_file_id, is_animated = await get_profile_photo_file_id(bot, entity_id)
                if photo_file_id:
                    if is_animated:
                        await loading_message.edit_media(
                            media=InputMediaAnimation(
                                media=photo_file_id,
                                caption=response
                            ),
                            reply_markup=buttons
                        )
                    else:
                        await loading_message.edit_media(
                            media=InputMediaPhoto(
                                media=photo_file_id,
                                caption=response
                            ),
                            reply_markup=buttons
                        )
                    LOGGER.info(f"Sent {chat_type.name.lower()} info with photo for {entity_id}")
                else:
                    await loading_message.edit_text(response, reply_markup=buttons)
                    LOGGER.info(f"Sent {chat_type.name.lower()} info without photo for {entity_id}")
            except Exception as e:
                LOGGER.error(f"Error sending {chat_type.name.lower()} info with photo for {entity_id}: {e}")
                await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
        except Exception as e:
            LOGGER.error(f"Error fetching chat {username} for user {message.from_user.id}: {e}")
            await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
