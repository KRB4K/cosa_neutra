from telegram import Update, ReplyKeyboardMarkup, KeyboardButton

import db
from locales import translate, Token
from static import DEFAULT_GAME, WORKING_LANGUAGES
from static import tokens as LANG_TOKENS
from utils import sliced

LANG_TOKENS_LOOKUP = {v:k for k,v in LANG_TOKENS.items()}

def ok(update: Update) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(translate(Token.OK, update))]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def yes_or_no(update: Update) -> ReplyKeyboardMarkup:

    buttons = [
        [KeyboardButton(translate(Token.YES, update)), KeyboardButton(translate(Token.NO, update))],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def roles(update: Update) -> ReplyKeyboardMarkup:
    role_keyboard = [
        [KeyboardButton(translate(Token.NEUTRALIZER_ROLE, update)), 
         KeyboardButton(translate(Token.REVIEWER_ROLE, update))],
        [KeyboardButton(translate(Token.HYBRID_ROLE, update))]
    ]
    role_markup = ReplyKeyboardMarkup(role_keyboard, resize_keyboard=True, one_time_keyboard=True)
    return role_markup

def working_languages(update: Update):
    keyboard  = [
        [KeyboardButton(translate(lang_token, update)) for lang_token in WORKING_LANGUAGES]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
    

async def teams(update: Update, game:str = DEFAULT_GAME):
    keyboard = []
    active_teams = await db.ASYNC.teams.find({'active':True,  'games':game}).to_list(None)
    for t in sliced(active_teams, 2):
        buttons = [KeyboardButton(t['name']) for t in t]
        keyboard.append(buttons)
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
