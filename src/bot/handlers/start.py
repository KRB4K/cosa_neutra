import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

import api.models as models
from api.main import load_active_user
from bot.handlers.onboarding import ask_language
from bot.utils import get_entities, _reset
from locales import translate, Token
from log import logger
import keyboards as keyboards
from states import STATES

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for /start command."""
    user_id = update.effective_user.id
    chat, message, user = get_entities(update)
    
    await _reset()

    active_user = await load_active_user(update, context)
    if not active_user:
        active_user = models.User.create_user(user, chat.id)
        print(active_user)
        logger.info(f"User {user_id} is new. Starting onboarding process.")
        return await ask_language(update, context)
    
    logger.info(f"User {user_id} has started the bot.")
    reply = translate(Token.WELCOME, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.main_menu(update)
    )
    return ConversationHandler.END