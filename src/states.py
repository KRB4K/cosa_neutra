from enum import Enum, auto

class STATES(str, Enum):
    ASK_LANGUAGE = auto()

    ASK_IF_IN_TEAM = auto()
    ASK_TEAM = auto()
    REGISTER_IN_TEAM = auto()

    ASK_ROLE = auto()
    END = auto()
    START_ONBOARDING = auto()
    FINISH_ONBOARDING = auto()
    PLAY = auto()
