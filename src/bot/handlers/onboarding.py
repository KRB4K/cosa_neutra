
from telegram import Update
from telegram.ext import CallbackContext


import api.enums
from api.main import load_active_user
from bot.utils import get_entities
import keyboards
from locales import translate, get_user_language, TRANSLATIONS, Token
import replies
from states import State, set_state, clear_state



async def ask_language(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's working language."""

    reply = translate(Token.ASK_LANGUAGE, context)
    # set_state(context, State.LANGUAGE_IS_ASKED)
    # return await update.message.reply_text(reply)
    # return await update.message.reply_text(reply, reply_markup=keyboards.working_languages(update))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup = keyboards.working_languages(context)
    )
    set_state(context, State.LANGUAGE_IS_ASKED)

async def set_language(update: Update, context: CallbackContext) -> int:
    _, message, _ = get_entities(update)
    user = await load_active_user(update, context)
    user_lang = get_user_language(update)
    allowed_inputs = list(TRANSLATIONS[user_lang].values())
    if not message.text in allowed_inputs:
        valid_inputs = ", ".join(allowed_inputs)
        await update.message.reply_text(
            f"Invalid language. Please select one of the following: {valid_inputs}"
        )
    user.update(working_language=message.text)
    set_state(context, State.HAS_TEAM_IS_ASKED)
    return await ask_if_in_team(update, context)
    

async def ask_if_in_team(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    reply = translate(Token.ASK_IF_IN_TEAM, context)
    
    set_state(context, State.HAS_TEAM_IS_ASKED)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup = keyboards.yes_or_no(context)
    )

async def process_has_team_response(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    msg = update.message.text
    print("is in team?", update.message.text)

    if msg == translate(Token.YES, context):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translate(Token.ASK_TEAM, context),
            reply_markup = await keyboards.teams(context)
        )
        set_state(context, State.IN_WHICH_TEAM_IS_ASKED)

    else:
        set_state(context, State.WHICH_ROLE_IS_ASKED)
        return await ask_role(update, context)
    

async def register_in_team(update: Update, context: CallbackContext) -> int:
    active_user = await load_active_user(update, context)
    print('In team', update.message.text)

    active_user.register_in_team(update.message.text)
    set_state(context, State.WHICH_ROLE_IS_ASKED)
    return await ask_role(update, context)


async def ask_role(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's role."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=translate(Token.ASK_ROLE, context),
        reply_markup=keyboards.roles(context)
    )
    # return STATES.FINISH_ONBOARDING

async def finish_onboarding(update: Update, context: CallbackContext) -> int:
    """Handler to finish onboarding process."""
    active_user = await load_active_user(update, context)

    msg = update.message.text
    if msg == translate(Token.NEUTRALIZER_ROLE, context):
        role = api.enums.Roles.neutralizer
    
    elif msg == translate(Token.REVIEWER_ROLE, context):
        role = api.enums.Roles.reviewer
    
    elif msg == translate(Token.HYBRID_ROLE, context):
        role = api.enums.Roles.hybrid
    
    else:
        raise ValueError("Invalid role")

    active_user.update(role=role)
    
    clear_state(context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies.main_menu(update, context)
    )