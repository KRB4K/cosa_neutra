import logging
from telegram import Update
from telegram.ext import CallbackContext

import api.enums
from api.main import load_active_user
from bot.utils import get_entities
import keyboards
from locales import translate, get_user_language, TRANSLATIONS, Token
import replies
from states import State, set_state, clear_state, set_current_lang
from bot.handlers import tutorial

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ask_language(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's working language."""
    logger.info("Asking for user's working language")
    reply = translate(Token.ASK_LANGUAGE, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.working_languages(context)
    )
    set_state(context, State.LANGUAGE_IS_ASKED)

async def set_language(update: Update, context: CallbackContext) -> int:
    logger.info("Setting user's language")
    _, message, _ = get_entities(update)
    user = await load_active_user(update, context)
    user_lang = get_user_language(context)
    allowed_inputs = list(TRANSLATIONS[user_lang].values())
    if not message.text in allowed_inputs:
        valid_inputs = ", ".join(allowed_inputs)
        await update.message.reply_text(
            f"Invalid language. Please select one of the following: {valid_inputs}"
        )
    lang = 'en'
    match message.text:
        case 'French':
            lang = 'fr'
        case 'English':
            lang = 'en'

    user.update(working_language=lang)
    set_current_lang(context, lang)
    reply = await tutorial.intro(update, context)
    return reply

async def ask_if_in_team(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    logger.info("Asking if user has a team")
    reply = translate(Token.ASK_IF_IN_TEAM, context)
    set_state(context, State.HAS_TEAM_IS_ASKED)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.yes_or_no(context)
    )

async def process_has_team_response(update: Update, context: CallbackContext) -> int:
    """Handler to process the response if the user has a team."""
    msg = update.message.text
    logger.info(f"User response to having a team: {msg}")

    if msg == translate(Token.YES, context):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translate(Token.ASK_TEAM, context),
            reply_markup=await keyboards.teams(context)
        )
        set_state(context, State.IN_WHICH_TEAM_IS_ASKED)
    else:
        set_state(context, State.WHICH_ROLE_IS_ASKED)
        return await ask_role(update, context)

async def register_in_team(update: Update, context: CallbackContext) -> int:
    logger.info("Registering user in team")
    active_user = await load_active_user(update, context)
    active_user.register_in_team(update.message.text)
    set_state(context, State.WHICH_ROLE_IS_ASKED)
    return await ask_role(update, context)

async def ask_role(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's role."""
    logger.info("Asking for user's role")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=translate(Token.ASK_ROLE, context),
        reply_markup=keyboards.roles(context)
    )

async def finish_onboarding(update: Update, context: CallbackContext) -> int:
    """Handler to finish onboarding process."""
    logger.info("Finishing onboarding process")
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

    active_user.update(role=role, active=True)
    clear_state(context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies.main_menu(update, context)
    )
