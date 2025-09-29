# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX
from utils.helpers import *

@bot.on_message(filters.command("me", prefixes=COMMAND_PREFIX.split("|")))
async def me_command(bot: Client, message):
    LOGGER.info(f"Me command received for user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Your Info...`")
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
        LOGGER.error(f"Error processing me command for user {message.from_user.id}: {e}")
        await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
