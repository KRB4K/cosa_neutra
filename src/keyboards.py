
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

import db
from locales import translate, Token
from static import DEFAULT_GAME, WORKING_LANGUAGES
from static import tokens as LANG_TOKENS
from utils import sliced

LANG_TOKENS_LOOKUP = {v:k for k,v in LANG_TOKENS.items()}


def yes_or_no(update: Update) -> InlineKeyboardMarkup:

    buttons = [
        [InlineKeyboardButton(translate(Token.YES, update)), InlineKeyboardButton(translate(Token.NO, update))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def main_menu(update: Update) -> InlineKeyboardMarkup:

    main_menu_keyboard = [
        [InlineKeyboardButton(translate(Token.PLAY_BUTTON, update), callback_data='play'), InlineKeyboardButton(translate(Token.HELP_BUTTON, update))],
        [InlineKeyboardButton(translate(Token.END_GAME_BUTTON, update)), InlineKeyboardButton(translate(Token.SHOW_SCORE_BUTTON, update))]
    ]
    main_menu_markup = InlineKeyboardMarkup(main_menu_keyboard)
    return main_menu_markup

def roles(update: Update) -> InlineKeyboardMarkup:
    role_keyboard = [
        [InlineKeyboardButton(translate(Token.NEUTRALIZER_ROLE, update)), 
         InlineKeyboardButton(translate(Token.REVIEWER_ROLE, update))],
        [InlineKeyboardButton(translate(Token.HYBRID_ROLE, update))]
    ]
    role_markup = InlineKeyboardMarkup(role_keyboard)
    return role_markup

def working_languages(update: Update):
    keyboard  = [
        [InlineKeyboardButton(translate(lang_token, update), callback_data=lang_token) for lang_token in WORKING_LANGUAGES]
    ]
    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard
    

async def teams(update: Update, game:str = DEFAULT_GAME):
    keyboard = []
    active_teams = await db.ASYNC.teams.find({'active':True,  'games':game}).to_list(None)
    for t in sliced(active_teams, 2):
        buttons = [InlineKeyboardButton(t['name']) for t in t]
        keyboard.append(buttons)
    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard

