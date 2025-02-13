from telegram import Update
from telegram.ext import ContextTypes
import logging

from api.main import load_active_user
from bot.handlers.fallbacks import default_handler
from bot.handlers import onboarding, play, tutorial, report
from bot.utils import get_entities
from locales import get_user_language, translate, Token
import replies
from states import State, get_state, get_current_lang, set_current_lang

logging.basicConfig(level=logging.INFO)

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    state = get_state(context)
    _, message, _ = get_entities(update)
    user = await load_active_user(update, context)
    user_lang = get_user_language(context)
    user_id = update.effective_user.id

    logging.info(f"User {user_id} in state {state}")

    match state:
        case State.NONE:
            logging.info(f"User {user_id} triggered default_handler")
            return await default_handler(update, context)
        
        case State.TUTO_INTRO_SENT:
            logging.info(f"User {user_id} in TUTO_INTRO_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.intro(update, context)
            return await tutorial.game_goal(update, context)
        
        case State.TUTO_GAME_GOAL_SENT:
            logging.info(f"User {user_id} in TUTO_GAME_GOAL_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.game_goal(update, context)
            return await tutorial.tuto_roles(update, context)
        
        case State.TUTO_ROLES_SENT:
            logging.info(f"User {user_id} in TUTO_ROLES_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_roles(update, context)
            return await tutorial.tuto_neutralizer(update, context)
        
        case State.TUTO_NEUTRALIZER_SENT:
            logging.info(f"User {user_id} in TUTO_NEUTRALIZER_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_neutralizer(update, context)
            return await tutorial.tuto_reviewer(update, context)
        
        case State.TUTO_REVIEWER_SENT:
            logging.info(f"User {user_id} in TUTO_REVIEWER_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_reviewer(update, context)
            return await tutorial.tuto_hybrid(update, context)
        
        case State.TUTO_HYBRID_SENT:
            logging.info(f"User {user_id} in TUTO_HYBRID_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_hybrid(update, context)
            return await tutorial.tuto_leaderboard(update, context)
        
        case State.TUTO_LEADERBOARD_SENT:
            logging.info(f"User {user_id} in TUTO_LEADERBOARD_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_leaderboard(update, context)
            return await tutorial.tuto_streak(update, context)
        
        case State.TUTO_STREAK_SENT:
            logging.info(f"User {user_id} in TUTO_STREAK_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_streak(update, context)
            return await tutorial.tuto_team(update, context)
        
        case State.TUTO_TEAM_SENT:
            logging.info(f"User {user_id} in TUTO_TEAM_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_team(update, context)
            return await tutorial.tuto_end(update, context)
        
        case State.TUTO_END_SENT:
            logging.info(f"User {user_id} in TUTO_END_SENT")
            if message.text != translate(Token.OK, context):
                return await tutorial.tuto_end(update, context)
            if not user.role:
                return await onboarding.ask_if_in_team(update, context)
            return await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=replies.main_menu(update, context)
            )
                
        case State.NEED_LANGUAGE:
            logging.info(f"User {user_id} in NEED_LANGUAGE")
            return await onboarding.ask_language(update, context)
        
        case State.LANGUAGE_IS_ASKED:
            logging.info(f"User {user_id} in LANGUAGE_IS_ASKED")
            return await onboarding.set_language(update, context)
        
        case State.HAS_TEAM_IS_ASKED:
            logging.info(f"User {user_id} in HAS_TEAM_IS_ASKED")
            return await onboarding.process_has_team_response(update, context)
        
        case State.IN_WHICH_TEAM_IS_ASKED:
            logging.info(f"User {user_id} in IN_WHICH_TEAM_IS_ASKED")
            return await onboarding.register_in_team(update, context)
        
        case State.WHICH_ROLE_IS_ASKED:
            logging.info(f"User {user_id} in WHICH_ROLE_IS_ASKED")
            return await onboarding.finish_onboarding(update, context)
        
        case State.HAS_ONGOING_TASK:
            logging.info(f"User {user_id} in HAS_ONGOING_TASK")
            return await play.register_task(update, context)
        
        case State.IS_REPORTING:
            logging.info(f"User {user_id} in IS_REPORTING")
            return await report.register_report(update, context)