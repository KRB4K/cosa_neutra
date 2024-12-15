import logging

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

from api.main import load_active_user
import api.models as models
import api.enums
import db
import keyboards
from states import State, set_state, get_state
from static import WORKING_LANGUAGES, DEFAULT_GAME

from locales import translate, Token

async def ask_language(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's working language."""

    reply = translate(Token.ASK_LANGUAGE, update)
    return await update.message.reply_text(reply)
    # return await update.message.reply_text("Please choose:", reply_markup=keyboards.working_languages(update))
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=reply,
    #     reply_markup = keyboards.working_languages(update)
    # )
    # set_state(context, State.LANGUAGE_IS_ASKED)

async def set_language(update: Update, context: CallbackContext) -> int:
    ...
    

async def ask_if_in_team(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    user_id = update.effective_user.id
    active_user = await load_active_user(update, context)
    active_user.update(lang=update.message.text)
    # user_states[user_id] = {"language": update.message.text}

    reply = translate(Token.ASK_IF_IN_TEAM, update)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup = keyboards.yes_or_no(update)
    )
    # return STATES.ASK_TEAM

async def ask_team(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    msg = update.message.text
    print("is in team?", update.message.text)

    if msg == translate(Token.YES, update):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translate(Token.ASK_TEAM, update),
            reply_markup = await keyboards.teams(update)
        )
        # return STATES.REGISTER_IN_TEAM

    else:
        return await ask_role(update, context)
    

async def register_in_team(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    active_user = await load_active_user(update, context)
    # user_states[user_id]["team"] = update.message.text
    print('In team', update.message.text)

    active_user.register_in_team(update.message.text)

    return await ask_role(update, context)


async def ask_role(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's role."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=translate(Token.ASK_ROLE, update),
        reply_markup=keyboards.roles(update)
    )
    # return STATES.FINISH_ONBOARDING

async def finish_onboarding(update: Update, context: CallbackContext) -> int:
    """Handler to finish onboarding process."""
    user_id = update.effective_user.id
    active_user = await load_active_user(update, context)

    msg = update.message.text
    if msg == translate(Token.NEUTRALIZER_ROLE, update):
        role = api.enums.Roles.neutralizer
    
    elif msg == translate(Token.REVIEWER_ROLE, update):
        role = api.enums.Roles.reviewer
    
    elif msg == translate(Token.HYBRID_ROLE, update):
        role = api.enums.Roles.hybrid
    
    else:
        raise ValueError("Invalid role")

    active_user.update(role=role)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=translate(Token.FINISH_ONBOARDING, update),
        reply_markup=keyboards.main_menu(update)
    )
    return ConversationHandler.END