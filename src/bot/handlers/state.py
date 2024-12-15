from states import State
from bot.handlers.fallbacks import default_handler, unknown_command_handler

from bot.handlers import onboarding

def handle_user_state(state: State):
    """Return the handler for the given state"""
    match state:
        case State.NONE:
            return default_handler
        
        case State.NEED_LANGUAGE:
            return onboarding.ask_language