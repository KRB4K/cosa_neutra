import logging

from click import clear
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

from api.main import load_active_user
import api.models as models
import api.enums
import db
import keyboards
import replies
from states import State, set_state, get_state, clear_state
from static import WORKING_LANGUAGES, DEFAULT_GAME

from bot.utils import get_entities

from locales import translate, get_user_language, TRANSLATIONS, Token

async def intro(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_INTRO, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_INTRO_SENT)

async def game_goal(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_GAME_GOAL, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_GAME_GOAL_SENT)

async def tuto_roles(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_ROLES, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_ROLES_SENT)

async def tuto_neutralizer(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_NEUTRALIZER, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_NEUTRALIZER_SENT)

async def tuto_reviewer(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_REVIEWER, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_REVIEWER_SENT)

async def tuto_hybrid(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_HYBRID, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_HYBRID_SENT)

async def tuto_leaderboard(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_LEADERBOARD, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_LEADERBOARD_SENT)

async def tuto_streak(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_STREAK, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_STREAK_SENT)

async def tuto_team(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_TEAM, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_TEAM_SENT)

async def tuto_end(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_END, update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(update)
    )
    set_state(context, State.TUTO_END_SENT)



