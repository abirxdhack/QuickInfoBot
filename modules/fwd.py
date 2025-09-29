from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from utils.helpers import *

def format_hidden_sender_response(sender_name):
    response = (
        "**🔍 Showing Forwarded User Info 📋**\n"
        "━━━━━━━━━━━━━━━━\n"
        f"**Name:** {sender_name}\n"
        "━━━━━━━━━━━━━━━━\n"
        "**👁 Thank You for Using Our Tool ✅**"
    )
    return response, sender_name

@bot.on_message(filters.private & filters.forwarded)
async def handle_forwarded_message(bot: Client, message):
    LOGGER.info(f"Forwarded message received from user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Forwarded Info...`")
    try:
        if hasattr(message, "forward_origin") and message.forward_origin:
            origin = message.forward_origin
            if hasattr(origin, "sender_user") and origin.sender_user:
                user = origin.sender_user
                response, full_name = format_user_response(user)
                entity_id = user.id
            elif hasattr(origin, "chat") and origin.chat:
                chat = origin.chat
                response, full_name = format_chat_response(chat)
                entity_id = chat.id
            elif hasattr(origin, "sender_user_name") and origin.sender_user_name:
                response, full_name = format_hidden_sender_response(origin.sender_user_name)
                entity_id = None
            else:
                response, full_name = format_hidden_sender_response("Unknown")
                entity_id = None
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=full_name, copy_text=str(entity_id) if entity_id else full_name)]]
            )
            try:
                photo_file_id, is_animated = await get_profile_photo_file_id(bot, entity_id) if entity_id else (None, False)
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
                    LOGGER.info(f"Sent forwarded info with photo for {entity_id if entity_id else 'hidden sender'}")
                else:
                    await loading_message.edit_text(response, reply_markup=buttons)
                    LOGGER.info(f"Sent forwarded info without photo for {entity_id if entity_id else 'hidden sender'}")
            except Exception as e:
                LOGGER.error(f"Error sending forwarded info for {entity_id if entity_id else 'hidden sender'}: {e}")
                await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
        else:
            response, full_name = format_hidden_sender_response("Unknown")
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=full_name, copy_text=full_name)]]
            )
            await loading_message.edit_text(response, reply_markup=buttons)
            LOGGER.info("Sent forwarded info for unknown origin")
    except Exception as e:
        LOGGER.error(f"Error handling forwarded message from user {message.from_user.id}: {e}")
        await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
