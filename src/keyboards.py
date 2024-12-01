
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

import db
from locales import translate, Token
from static import DEFAULT_GAME, WORKING_LANGUAGES
from utils import sliced




def yes_or_no(update: Update) -> ReplyKeyboardMarkup:

    buttons = [
        [InlineKeyboardButton(translate(Token.YES, update)), InlineKeyboardButton(translate(Token.NO, update))],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def main_menu(update: Update) -> ReplyKeyboardMarkup:

    main_menu_keyboard = [
        [InlineKeyboardButton(translate(Token.PLAY_BUTTON, update), callback_data='play'), InlineKeyboardButton(translate(Token.HELP_BUTTON, update))],
        [InlineKeyboardButton(translate(Token.END_GAME_BUTTON, update)), InlineKeyboardButton(translate(Token.SHOW_SCORE_BUTTON, update))]
    ]
    main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True, one_time_keyboard=True)
    return main_menu_markup

def roles(update: Update) -> ReplyKeyboardMarkup:
    role_keyboard = [
        [InlineKeyboardButton(translate(Token.NEUTRALIZER_ROLE, update)), 
         InlineKeyboardButton(translate(Token.REVIEWER_ROLE, update))],
        [InlineKeyboardButton(translate(Token.HYBRID_ROLE, update))]
    ]
    role_markup = ReplyKeyboardMarkup(role_keyboard, resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    return role_markup

def working_languages(update: Update):
    keyboard  = [
        [InlineKeyboardButton(translate(lang_token, update)) for lang_token in WORKING_LANGUAGES]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
    

async def teams(update: Update, game:str = DEFAULT_GAME):
    keyboard = []
    active_teams = await db.ASYNC.teams.find({'active':True,  'games':game}).to_list(None)
    for t in sliced(active_teams, 2):
        buttons = [InlineKeyboardButton(t['name']) for t in t]
        keyboard.append(buttons)
    keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

