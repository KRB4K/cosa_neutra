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

dotenv.load_dotenv()
BOT_TOKEN: str = os.getenv('telegram_bot_token')
GAME_NAME: str = os.getenv('game_name')
assert all((BOT_TOKEN, GAME_NAME)), 'Envrionment variables missing'

TELEGRAM_API = 'https://api.telegram.org'

user_states = {id:{} for id in models.get_existing_users_ids()}


async def get(url, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, *args, **kwargs)
        return response.json()
    
async def post(url: str, data: dict, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, *args, **kwargs)
        return response.json()  



async def send_notification(chat: Chat, message:str):
    url = TELEGRAM_API + f'/bot{BOT_TOKEN}/sendMessage'
    # message = urllib.parse.quote_plus(message)
    params = {
        'chat_id':chat.id,
    }
    body = {
        'text':message
    }
    response = await post(url, body, params=params)
    return response


from telegram.ext import CallbackQueryHandler

async def cb_QueryHandler(update: Update, context: CallbackContext):
    print('in test_CallbackQueryHandler')
    print(update.callback_query.data)
    await update.callback_query.answer()
    print('ooooo')
    await update.callback_query.edit_message_text(text=f"Selected option: {update.callback_query.data}")

    # await update.callback_query.edit_message_text(text="Selected option: {}".format(update.callback_query.data))

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    
    application.add_handler(onboarding_handler)
    
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_handler))
    application.add_handler(CallbackQueryHandler(cb_QueryHandler))    
    
    application.run_polling()