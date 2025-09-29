from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from utils.helpers import *

@bot.on_message(filters.private & filters.regex(r"^@.{4,32}$"))
async def username_command(bot: Client, message):
    LOGGER.info(f"Username message received from user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Username To Info...`")
    username = message.text.strip()
    try:
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
