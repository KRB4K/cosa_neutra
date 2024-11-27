from __future__ import annotations

from enum import Enum, auto

import telegram

DEFAULT = 'en'

def translate(token:Token, update:telegram.Update):
    lang = update.effective_user.language_code
    lang = lang if lang in TRANSLATIONS else DEFAULT
    try:
        translation = TRANSLATIONS[lang][token]
    except KeyError:
        translation = TRANSLATIONS[DEFAULT][token]
    return translation


class Token(Enum):

    YES = auto()
    NO = auto()

    # Menu
    WELCOME = auto()

    # Languages
    FRENCH = auto()
    ENGLISH = auto()

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
    ASK_IF_IN_TEAM = auto(),
    ASK_TEAM = auto()
    ASK_ROLE = auto()
    FINISH_ONBOARDING = auto()
    START_EXISTING_USER = auto()
    START_NEW_USER = auto()


TRANSLATIONS = {
    'en': {
        Token.YES: 'Yes',
        Token.NO: 'No',

        Token.FRENCH: 'French',
        Token.ENGLISH: 'English',

        Token.WELCOME: 'Welcome!',
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
        Token.ASK_IF_IN_TEAM: "Are you in a team?",
        Token.ASK_TEAM: "What is  your team?",
        Token.ASK_ROLE: "What is your role?",
        Token.FINISH_ONBOARDING: "Thank you! You are all set. Use /play to start playing!",
        Token.START_EXISTING_USER: "Welcome back! Use /play to start playing!",
        Token.START_NEW_USER: "Welcome to the game, let's start with a few questions!"
    },
    'fr': {
        Token.YES: 'Oui',
        Token.NO: 'Non',

        Token.FRENCH: 'Français',
        Token.ENGLISH: 'Anglais',

        Token.WELCOME: 'Bienvenue !',
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
        Token.ASK_IF_IN_TEAM: "Es-tu dans une équipe ?",
        Token.ASK_TEAM: "Quelle est ton équipe ?",
        Token.ASK_ROLE: "Quel est votre rôle ?",
        Token.FINISH_ONBOARDING: "Merci ! Vous êtes prêt. Utilisez /play pour commencer à jouer !",
        Token.START_EXISTING_USER: "Bon retour ! Utilisez /play pour commencer à jouer !",
        Token.START_NEW_USER: "Bienvenue dans le jeu, commençons par quelques questions !"
    }
}