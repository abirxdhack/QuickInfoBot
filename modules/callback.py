# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from utils import LOGGER
from miscs.adbtn import admin_buttons
from miscs.mybtn import my_buttons
from miscs.startbtn import menu_buttons
from bot import bot

@bot.on_message(filters.text & filters.regex(r"^👥 Admins Chat$"))
async def admin_button_handler(bot: Client, message):
    LOGGER.info("Admins Chat button clicked")
    await message.reply_text(
        "**🛡️ Channels and Groups Where You Are Admin**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a channel or group where you have admin privileges.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        reply_markup=admin_buttons
    )

@bot.on_message(filters.text & filters.regex(r"^👑 Owner Chat$"))
async def owner_button_handler(bot: Client, message):
    LOGGER.info("Owner Chat button clicked")
    await message.reply_text(
        "**📚 Your Channels and Groups**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share your channel or group.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        reply_markup=my_buttons
    )

@bot.on_message(filters.text & filters.regex(r"^🔙 Back$"))
async def back_button_handler(bot: Client, message):
    LOGGER.info("Back button clicked")
    await message.reply_text(
        "**👋 Welcome to Chat ID Finder Bot!** 🆔\n\n"
        "**✅ Fetch Any Chat ID Instantly!**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 **Features:**\n"
        "- Supports users, bots, private/public groups & channels\n"
        "- Fast and reliable\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        reply_markup=menu_buttons
    )
