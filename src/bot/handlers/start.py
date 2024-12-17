import logging

from httpx import get
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

import api.models as models
from api.main import load_active_user
from bot.handlers import onboarding, tutorial
from bot.utils import get_entities, _reset
import keyboards
from locales import translate, Token
from log import logger
import replies
from states import State, get_state, set_state, clear_state, clear_current_to_do

async def say_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = translate(Token.WELCOME, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
    )

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for /start command."""
    user_id = update.effective_user.id
    chat, message, user = get_entities(update)
    
    clear_state(context)
    clear_current_to_do(context)
    # await _reset()

    logger.info(f"User {user_id} has started the bot.")
    await say_welcome(update, context)

    active_user = await load_active_user(update, context)
    if active_user:
        team  = active_user.get_team()
    if not active_user:
        active_user = models.User.create_user(user, chat.id)
        reply = await tutorial.intro(update, context)
        return reply
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies.main_menu(update, context)
    )