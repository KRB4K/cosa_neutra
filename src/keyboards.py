from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

import db
from locales import translate, Token
from static import DEFAULT_GAME, WORKING_LANGUAGES
from utils import sliced

def ok(context: ContextTypes.DEFAULT_TYPE) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(translate(Token.OK, context))]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def yes_or_no(context: ContextTypes.DEFAULT_TYPE) -> ReplyKeyboardMarkup:

    buttons = [
        [KeyboardButton(translate(Token.YES, context)), KeyboardButton(translate(Token.NO, context))],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def roles(context: ContextTypes.DEFAULT_TYPE) -> ReplyKeyboardMarkup:
    role_keyboard = [
        [KeyboardButton(translate(Token.NEUTRALIZER_ROLE, context)), 
         KeyboardButton(translate(Token.REVIEWER_ROLE, context))],
        [KeyboardButton(translate(Token.HYBRID_ROLE, context))]
    ]
    role_markup = ReplyKeyboardMarkup(role_keyboard, resize_keyboard=True, one_time_keyboard=True)
    return role_markup

def working_languages(context: ContextTypes.DEFAULT_TYPE):
    keyboard  = [
        [KeyboardButton(translate(lang_token, context)) for lang_token in WORKING_LANGUAGES]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
    

async def teams(context: ContextTypes.DEFAULT_TYPE, game:str = DEFAULT_GAME):
    keyboard = []
    active_teams = await db.ASYNC.teams.find({'active':True,  'games':game}).to_list(None)
    for t in sliced(active_teams, 2):
        buttons = [KeyboardButton(t['name']) for t in t]
        keyboard.append(buttons)
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
