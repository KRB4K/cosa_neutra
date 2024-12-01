from enum import Enum, auto
import os
import logging
import urllib
import urllib.parse
import httpx

import dotenv
import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

from bot.handlers.main import onboarding as onboarding_handler
from bot.handlers.main import unknown_command_handler, default_handler


import api.models as models

from settings import BOT_TOKEN, GAME_NAME
assert all((BOT_TOKEN, GAME_NAME)), 'Envrionment variables missing'

    # await update.callback_query.edit_message_text(text="Selected option: {}".format(update.callback_query.data))

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    
    application.add_handler(onboarding_handler)
    
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_handler))
    
    application.run_polling()