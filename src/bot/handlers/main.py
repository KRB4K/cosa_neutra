import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

import api.models as models
import db
from log import logger
from states import State
from static import WORKING_LANGUAGES, DEFAULT_GAME

from bot.handlers.onboarding import ask_if_in_team, ask_team, register_in_team, ask_role, finish_onboarding
from bot.handlers.start import start_handler
from bot.handlers.fallbacks import default_handler, unknown_command_handler






async def _reset():
    global user_states
    user_states = {}
    pierre = 6384730936
    await models.User.ax_coll.delete_one({'id':pierre})
    await db.ASYNC.team_members.delete_one({
            "player":pierre,
            "game": DEFAULT_GAME
        })
    

# onboarding = ConversationHandler(
#     entry_points=[CommandHandler('start', start)],
#     states={
#         STATES.ASK_IF_IN_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_if_in_team)],
#         STATES.ASK_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_team)],
#         STATES.REGISTER_IN_TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_in_team)],
#         STATES.ASK_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_role)],
#         STATES.FINISH_ONBOARDING: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_onboarding)],
#     },
#     fallbacks=[CommandHandler('start', start)])