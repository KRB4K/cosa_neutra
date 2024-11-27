import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

import api.models as models
import db
from log import logger
from states import STATES
from static import WORKING_LANGUAGES, DEFAULT_GAME

from bot.handlers.onboarding import ask_if_in_team, ask_team, register_in_team, ask_role, finish_onboarding
from bot.handlers.start import start



async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.") # type: ignore

async def default_handler(update: Update, context: CallbackContext) -> None:
    """Handler for any non-command messages."""
    user_message = update.message.text
    logger.info(f"Received message: {user_message} from user: {update.effective_user.id}")

    # Here you can parse the input or trigger other kinds of actions
    if "hello" in user_message.lower():
        await update.message.reply_text("Hi there! How can I assist you today?")
    else:
        await update.message.reply_text("I'm not sure how to respond to that. Try using /help.")



async def _reset():
    global user_states
    user_states = {}
    pierre = 6384730936
    await models.User.ax_coll.delete_one({'id':pierre})
    await db.ASYNC.team_members.delete_one({
            "player":pierre,
            "game": DEFAULT_GAME
        })
    

onboarding = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        STATES.ASK_IF_IN_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_if_in_team)],
        STATES.ASK_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_team)],
        STATES.REGISTER_IN_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_in_team)],
        STATES.ASK_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_role)],
        STATES.FINISH_ONBOARDING: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_onboarding)],
    },
    fallbacks=[CommandHandler('start', start)])