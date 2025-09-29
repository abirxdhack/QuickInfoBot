# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from bot import bot
from utils import LOGGER
from core.start import start
from modules.help import help_command
from modules.my import my_command
from modules.admin import admin_command
from modules.me import me_command
from modules.info import info_command
from modules.link import link_command
from modules.fwd import handle_forwarded_message
from modules.username import username_command
from modules.inline import inline_query_handler, chosen_inline_result
from modules.callback import admin_button_handler, owner_button_handler
from shared.chatinfo import handle_message

LOGGER.info("QuickInfoBot Started Successfully 💥")
bot.run()