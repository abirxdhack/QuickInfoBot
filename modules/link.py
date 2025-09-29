# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX
from utils.helpers import *

@bot.on_callback_query(filters.regex(r"^get_link_(\d+|-?\d+)$"))
async def handle_link_callback(bot: Client, callback_query):
    entity_id = int(callback_query.data.split("_")[-1])
    try:
        chat = await bot.get_chat(entity_id)
        chat_type = chat.type
        is_group_context = chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]
        if chat_type in [ChatType.PRIVATE, ChatType.BOT]:
            entity = await bot.get_users(entity_id)
            response, full_name = format_user_response(entity, is_group_context, chat if is_group_context else None)
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Android Link", url=f"tg://openmessage?user_id={entity.id}"),
                        InlineKeyboardButton(text="IOS Link", url=f"https://t.me/@id{entity.id}")
                    ],
                    [InlineKeyboardButton(text=full_name, user_id=entity.id)]
                ]
            )
        else:
            entity = chat
            response, full_name = format_chat_response(chat)
            chat_id_without_prefix = str(chat.id).replace("-100", "")
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Join Link", url=f"https://t.me/c/{chat_id_without_prefix}/10000000")]]
            )
        try:
            photo_file_id, is_animated = await get_profile_photo_file_id(bot, entity_id)
            if photo_file_id:
                if is_animated:
                    await callback_query.message.edit_media(
                        media=InputMediaAnimation(
                            media=photo_file_id,
                            caption=response
                        ),
                        reply_markup=buttons
                    )
                else:
                    await callback_query.message.edit_media(
                        media=InputMediaPhoto(
                            media=photo_file_id,
                            caption=response
                        ),
                        reply_markup=buttons
                    )
                LOGGER.info(f"Edited {chat_type.name.lower()} info with link buttons for {entity_id}")
            else:
                await callback_query.message.edit_text(response, reply_markup=buttons)
                LOGGER.info(f"Edited {chat_type.name.lower()} info with link buttons without photo for {entity_id}")
        except Exception as e:
            LOGGER.error(f"Error editing {chat_type.name.lower()} info with link buttons for {entity_id}: {e}")
            await callback_query.message.edit_text("**Looks Like I Don't Have Control Over The Entity**")
    except Exception as e:
        LOGGER.error(f"Error processing link callback for {entity_id}: {e}")
        await callback_query.message.edit_text("**Looks Like I Don't Have Control Over The Entity**")

@bot.on_message(filters.command(["link"], prefixes=COMMAND_PREFIX.split("|")))
async def link_command(bot: Client, message):
    LOGGER.info(f"Link command received from user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Link...`")
    command_parts = message.text.split()
    if len(command_parts) == 1 or (len(command_parts) > 1 and command_parts[1].lower() == 'me'):
        try:
            user = message.from_user
            response, full_name = format_user_response(user)
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Get Chat Link", callback_data=f"get_link_{user.id}")]]
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
                    LOGGER.info(f"Sent user link info with photo for user {user.id}")
                else:
                    await loading_message.edit_text(response, reply_markup=buttons)
                    LOGGER.info(f"Sent user link info without photo for user {user.id}")
            except Exception as e:
                LOGGER.error(f"Error sending user link info with photo for user {user.id}: {e}")
                await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
        except Exception as e:
            LOGGER.error(f"Error processing link command for user {message.from_user.id}: {e}")
            await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
    elif len(command_parts) > 1 and command_parts[1].lower() != 'me':
        LOGGER.info("Extracting username from the command")
        username = command_parts[1].strip('@').replace('https://', '').replace('http://', '').replace('t.me/', '').replace('/', '').replace(':', '')
        try:
            LOGGER.info(f"Fetching link info for user or bot: {username}")
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
                [[InlineKeyboardButton(text="Get Chat Link", callback_data=f"get_link_{entity_id}")]]
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
                    LOGGER.info(f"Sent {chat_type.name.lower()} link info with photo for {entity_id}")
                else:
                    await loading_message.edit_text(response, reply_markup=buttons)
                    LOGGER.info(f"Sent {chat_type.name.lower()} link info without photo for {entity_id}")
            except Exception as e:
                LOGGER.error(f"Error sending {chat_type.name.lower()} link info with photo for {entity_id}: {e}")
                await loading_message.edit_text("**Looks Like I Don't Have Control Over The Entity**")
        except Exception as e:
            LOGGER.error(f"Error fetching chat {username} for user {message.from_user.id}: {e}")
            await loading_message.edit_text("**Looks Like I Don't Have Control Over The Entity**")
