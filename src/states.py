from enum import Enum, auto

from telegram.ext import CallbackContext

from log import logger

class State(Enum):
    """Enum for storing user states"""
    NONE = auto()
    NEED_LANGUAGE = auto()
    LANGUAGE_IS_ASKED = auto()
    HAS_TEAM = auto()
    NEED_TEAM = auto()
    NEED_ROLE = auto()


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
