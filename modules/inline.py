# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from modules.info import format_user_response, format_chat_response, get_profile_photo_file_id
from utils import LOGGER
from bot import bot

async def get_bot_username():
    bot_user = await bot.get_me()
    return f"@{bot_user.username}"

@bot.on_inline_query()
async def inline_query_handler(client: Client, query):
    LOGGER.info(f"Inline query received from user {query.from_user.id}: {query.query}")
    bot_username = await get_bot_username()
    if not query.query:
        results = [
            InlineQueryResultArticle(
                id="placeholder",
                title="Enter a username",
                input_message_content=InputTextMessageContent(f"**Please enter a username after {bot_username} (e.g., {bot_username} @username)**"),
                description="Type a username to get info",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat="")],
                        [InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")]
                    ]
                )
            )
        ]
        await query.answer(results=results, cache_time=1)
        LOGGER.info("Sent placeholder result for empty query")
        return
    username = query.query.strip().strip('@').replace('https://', '').replace('http://', '').replace('t.me/', '').replace('/', '').replace(':', '')
    try:
        chat = await client.get_chat(username)
        entity_id = chat.id
        chat_type = chat.type
        is_group_context = chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]
        if chat_type in [ChatType.PRIVATE, ChatType.BOT]:
            entity = await client.get_users(entity_id)
            response, full_name = format_user_response(entity, is_group_context, chat if is_group_context else None)
        else:
            entity = chat
            response, full_name = format_chat_response(chat)
        results = [
            InlineQueryResultArticle(
                id=str(entity_id),
                title=full_name,
                input_message_content=InputTextMessageContent(
                    message_text=response,
                    entities=await client.get_chat(entity_id).get_caption_entities() if hasattr(await client.get_chat(entity_id), 'get_caption_entities') else None
                ),
                description=f"ID: {entity_id}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text=full_name, copy_text=str(entity_id))],
                        [
                            InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat=""),
                            InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")
                        ]
                    ]
                )
            )
        ]
        await query.answer(results=results, cache_time=1)
        LOGGER.info(f"Sent inline query results for {username} (ID: {entity_id})")
    except Exception as e:
        LOGGER.error(f"Error processing inline query for {username}: {e}")
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id="error",
                    title="Error",
                    input_message_content=InputTextMessageContent("**Looks Like I Don't Have Control Over The User**"),
                    description="Could not fetch user or chat info",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat="")],
                            [InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")]
                        ]
                    )
                )
            ],
            cache_time=1
        )

@bot.on_chosen_inline_result()
async def chosen_inline_result(client: Client, chosen_result):
    LOGGER.info(f"Chosen inline result for result_id: {chosen_result.result_id} by user {chosen_result.from_user.id}")
    bot_username = await get_bot_username()
    try:
        entity_id = int(chosen_result.result_id) if chosen_result.result_id not in ["error", "placeholder"] else None
        if not entity_id:
            if chosen_result.result_id == "placeholder":
                await client.send_message(
                    chat_id=chosen_result.from_user.id,
                    text=f"**Please enter a username after {bot_username} (e.g., {bot_username} @username)**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat="")],
                            [InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")]
                        ]
                    )
                )
                LOGGER.info("Sent placeholder message for chosen empty query")
            elif chosen_result.result_id == "error":
                await client.send_message(
                    chat_id=chosen_result.from_user.id,
                    text="**Looks Like I Don't Have Control Over The User**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat="")],
                            [InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")]
                        ]
                    )
                )
                LOGGER.info("Sent error message for chosen invalid query")
            return
        chat = await client.get_chat(entity_id)
        chat_type = chat.type
        is_group_context = chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]
        if chat_type in [ChatType.PRIVATE, ChatType.BOT]:
            entity = await client.get_users(entity_id)
            response, full_name = format_user_response(entity, is_group_context, chat if is_group_context else None)
        else:
            entity = chat
            response, full_name = format_chat_response(chat)
        photo_file_id, is_animated = await get_profile_photo_file_id(client, entity_id)
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=full_name, copy_text=str(entity_id))],
                [
                    InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat=""),
                    InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")
                ]
            ]
        )
        if photo_file_id:
            try:
                if is_animated:
                    await client.send_animation(
                        chat_id=chosen_result.from_user.id,
                        animation=photo_file_id,
                        caption=response,
                        reply_markup=buttons
                    )
                    LOGGER.info(f"Sent chosen result with animation for {entity_id}")
                else:
                    await client.send_photo(
                        chat_id=chosen_result.from_user.id,
                        photo=photo_file_id,
                        caption=response,
                        reply_markup=buttons
                    )
                    LOGGER.info(f"Sent chosen result with photo for {entity_id}")
            except Exception as e:
                LOGGER.error(f"Error sending photo/animation for {entity_id}: {e}")
                await client.send_message(
                    chat_id=chosen_result.from_user.id,
                    text=response,
                    reply_markup=buttons
                )
                LOGGER.info(f"Sent chosen result without photo due to error for {entity_id}")
        else:
            await client.send_message(
                chat_id=chosen_result.from_user.id,
                text=response,
                reply_markup=buttons
            )
            LOGGER.info(f"Sent chosen result without photo for {entity_id}")
    except Exception as e:
        LOGGER.error(f"Error processing chosen inline result: {e}")
        await client.send_message(
            chat_id=chosen_result.from_user.id,
            text="**Looks Like I Don't Have Control Over The User**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="🔍 Search", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton(text="🔍 Search in Chat", switch_inline_query="")]
                ]
            )
        )
        LOGGER.info("Sent error message for chosen inline result failure")
