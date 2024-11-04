from __future__ import annotations

from enum import Enum, auto

from models.users import User

DEFAULT = 'en'

def translate(token:Token, user:User):
    lang = user.language if user else DEFAULT
    lang = lang if lang in TRANSLATIONS else DEFAULT
    return TRANSLATIONS[lang][token]


class Token(Enum):
    # Buttons
    PLAY_BUTTON = auto()
    HELP_BUTTON = auto()
    END_GAME_BUTTON = auto()
    SHOW_SCORE_BUTTON = auto()

    # Roles
    NEUTRALIZER_ROLE = auto()
    REVIEWER_ROLE = auto()
    HYBRID_ROLE = auto()

    # Other tokens
    TODAYS_MWE = auto()
    SUBMIT = auto()
    REVIEW = auto()
    CHANGE_LANGUAGE = auto()
    SHOW_SCOREBOARD = auto()

    # Messages
    UNKNOWN_COMMAND = auto()
    DEFAULT_GREETING = auto()
    DEFAULT_UNKNOWN = auto()
    ASK_LANGUAGE = auto()
    ASK_TEAM = auto()
    ASK_ROLE = auto()
    FINISH_ONBOARDING = auto()
    START_EXISTING_USER = auto()
    START_NEW_USER = auto()


TRANSLATIONS = {
    'en': {
        Token.PLAY_BUTTON: 'Play',
        Token.HELP_BUTTON: 'Help',
        Token.END_GAME_BUTTON: 'End Game',
        Token.SHOW_SCORE_BUTTON: 'Show Score',
        Token.NEUTRALIZER_ROLE: 'Neutralizer',
        Token.REVIEWER_ROLE: 'Reviewer',
        Token.HYBRID_ROLE: 'Hybrid',
        Token.TODAYS_MWE: "Today's MWE",
        Token.SUBMIT: 'Submit',
        Token.REVIEW: 'Review',
        Token.CHANGE_LANGUAGE: 'Change Language',
        Token.SHOW_SCOREBOARD: 'Show Scoreboard',
        
        # Messages
        Token.UNKNOWN_COMMAND: "Sorry, I didn't understand that command.",
        Token.DEFAULT_GREETING: "Hi there! How can I assist you today?",
        Token.DEFAULT_UNKNOWN: "I'm not sure how to respond to that. Try using /help.",
        Token.ASK_LANGUAGE: "Hello! I need to ask you a few questions to get started. What is your working language?",
        Token.ASK_TEAM: "Do you have a team? If so, which one?",
        Token.ASK_ROLE: "What is your role?",
        Token.FINISH_ONBOARDING: "Thank you! You are all set. Use /play to start playing!",
        Token.START_EXISTING_USER: "Welcome back! Use /play to start playing!",
        Token.START_NEW_USER: "Welcome to the game, let's start with a few questions!"
    },
    'fr': {
        Token.PLAY_BUTTON: 'Jouer',
        Token.HELP_BUTTON: 'Aide',
        Token.END_GAME_BUTTON: 'Terminer le jeu',
        Token.SHOW_SCORE_BUTTON: 'Afficher le score',
        Token.NEUTRALIZER_ROLE: 'Neutraliseur',
        Token.REVIEWER_ROLE: 'Réviseur',
        Token.HYBRID_ROLE: 'Hybride',
        Token.TODAYS_MWE: "MWE d'aujourd'hui",
        Token.SUBMIT: 'Soumettre',
        Token.REVIEW: 'Réviser',
        Token.CHANGE_LANGUAGE: 'Changer de langue',
        Token.SHOW_SCOREBOARD: 'Afficher le tableau des scores',

        # Messages
        Token.UNKNOWN_COMMAND: "Désolé, je n'ai pas compris cette commande.",
        Token.DEFAULT_GREETING: "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
        Token.DEFAULT_UNKNOWN: "Je ne sais pas comment répondre à cela. Essayez d'utiliser /help.",
        Token.ASK_LANGUAGE: "Bonjour ! Je dois vous poser quelques questions pour commencer. Quelle est votre langue de travail ?",
        Token.ASK_TEAM: "Avez-vous une équipe ? Si oui, laquelle ?",
        Token.ASK_ROLE: "Quel est votre rôle ?",
        Token.FINISH_ONBOARDING: "Merci ! Vous êtes prêt. Utilisez /play pour commencer à jouer !",
        Token.START_EXISTING_USER: "Bon retour ! Utilisez /play pour commencer à jouer !",
        Token.START_NEW_USER: "Bienvenue dans le jeu, commençons par quelques questions !"
    }
}