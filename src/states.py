from enum import Enum, auto

from telegram.ext import CallbackContext

from log import logger

class State(Enum):
    """Enum for storing user states"""
    NONE = auto()
    NEED_LANGUAGE = auto()
    LANGUAGE_IS_ASKED = auto()
    MUST_ASK_HAS_TEAM = auto()
    HAS_TEAM_IS_ASKED = auto()
    IN_WHICH_TEAM_IS_ASKED = auto()
    WHICH_ROLE_IS_ASKED = auto()
    HAS_ONGOING_TASK = auto()

    TUTO_INTRO_SENT = auto()
    TUTO_GAME_GOAL_SENT = auto()
    TUTO_ROLES_SENT = auto()
    TUTO_NEUTRALIZER_SENT = auto()
    TUTO_REVIEWER_SENT = auto()
    TUTO_HYBRID_SENT = auto()
    TUTO_LEADERBOARD_SENT = auto()
    TUTO_STREAK_SENT = auto()
    TUTO_TEAM_SENT = auto()
    TUTO_END_SENT = auto()
    


def set_current_to_do(context: CallbackContext, to_do:str) -> None:
    context.user_data["task"] = to_do  # type: ignore
    logger.info(f"Current task set to: {to_do}")


def get_current_to_do(context: CallbackContext) -> str:
    if "task" in context.user_data: # type: ignore
        return context.user_data["task"] # type: ignore
    else:
        set_current_to_do(context, "")
        return ""
    
def clear_current_to_do(context: CallbackContext) -> None:
    set_current_to_do(context, "")
    logger.info("Current task cleared")



def clear_state(context: CallbackContext) -> None:
    set_state(context, State.NONE)
    logger.info("State cleared")


def set_state(context: CallbackContext, state: State) -> None:
    context.user_data["state"] = state  # type: ignore
    logger.info(f"State set to: {state}")


def get_state(context: CallbackContext) -> State:
    if "state" in context.user_data: # type: ignore
        return context.user_data["state"] # type: ignore
    else:
        set_state(context, State.NONE)
        return State.NONE
