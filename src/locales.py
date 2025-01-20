from __future__ import annotations

from enum import Enum, auto
import states

import telegram
from telegram.ext import ContextTypes

DEFAULT = 'en'

def get_user_language(context: ContextTypes.DEFAULT_TYPE):
    lang = states.get_current_lang(context)
    lang = lang if lang in TRANSLATIONS else DEFAULT
    return lang

def translate(token:Token, context:ContextTypes.DEFAULT_TYPE, lang:str=None):
    if not lang:
        lang = get_user_language(context)
    try:
        translation = TRANSLATIONS[lang][token]
    except KeyError:
        translation = TRANSLATIONS[DEFAULT][token]
    return translation


class Token(Enum):

    OK = auto()
    YES = auto()
    NO = auto()

    # Menu
    WELCOME = auto()

    # Tutorial
    TUTO_INTRO = auto()
    TUTO_GAME_GOAL = auto()
    TUTO_ROLES = auto()
    TUTO_NEUTRALIZER = auto()
    TUTO_REVIEWER = auto()
    TUTO_HYBRID = auto()
    TUTO_LEADERBOARD = auto()
    TUTO_STREAK = auto()
    TUTO_TEAM = auto()
    TUTO_END = auto()

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

    # Messages
    UNKNOWN_COMMAND = auto()
    UNKNOWN_MESSAGE = auto()
    DEFAULT_GREETING = auto()
    DEFAULT_UNKNOWN = auto()

    ASK_LANGUAGE = auto()
    ASK_IF_IN_TEAM = auto(),
    ASK_TEAM = auto()
    ASK_ROLE = auto()
    FINISH_ONBOARDING = auto()

    START_EXISTING_USER = auto()
    START_NEW_USER = auto()

    MAIN_MENU_INTRO = auto()
    MAIN_MENU_PLAY = auto()
    MAIN_MENU_HELP = auto()
    MAIN_MENU_END_GAME = auto()
    MAIN_MENU_LEADERBOARD = auto()

    NOTHING_TO_DO = auto()
    NEUTRALIZE_THIS = auto()
    REVIEW_THIS = auto()
    SUCCESSFUL_NEW_NEUTRALIZATION = auto()
    SUCCESSFUL_NEW_REVIEW = auto()
    COULD_NOT_SAVE_SUBMISSION = auto()

    LIMIT_REACHED = auto()



TRANSLATIONS = {
    'en': {

        Token.OK: 'OK',
        Token.YES: 'Yes',
        Token.NO: 'No',

        Token.FRENCH: 'French',
        Token.ENGLISH: 'English',

        Token.TUTO_INTRO: "Welcome to the game tutorial! Here you will learn how to play.",
        Token.TUTO_GAME_GOAL: "The goal of the game is to render video game translations gender-agnostic. This means the sentences should not have any gender marker. This is what we call 'Neutralizing'.",
        Token.TUTO_ROLES: "To enhance the quality of submissions, there are two roles in the game: Neutralizer and Reviewer.",
        Token.TUTO_NEUTRALIZER: "Neutralizers are responsible for neutralizing the text. If you are a neutralizer, your goal is to provide the best gender-agnostic alternative translation. Just type it in the chat and send it. If the segment does not require any modification, copy and paste the original segment in the chat and send it.",
        Token.TUTO_REVIEWER: "Reviewers are responsible for reviewing the neutralizations. If you are a reviewer, your goal is to pick the best neutralization from the list you will be given. Just copy and paste the one you think is best in the chat and send it.",
        Token.TUTO_HYBRID: "On top of neutralizers and reviewers, a player can also be a hybrid. This means they play both roles simultaneously: they will be assigned a neutralization or a review at random. However, they will not be able to review their own neutralizations.",
        Token.TUTO_LEADERBOARD: "The leaderboard shows the player's scores. Neutralizing and reviewing always grants points. If you're a neutralizer, bonus points are granted if reviewers picked your neutralization the most. If you're a reviewer, bonus points are granted if your chosen best sentence was the one most picked by other reviewers.",
        Token.TUTO_STREAK: "Each day, you will receive a Telegram notification to come play. You will get a streak bonus if you play multiple days in a row. The longer the streak, the bigger the bonus.",
        Token.TUTO_TEAM: "Players can be part of a team (or choose to play solo). There is a leaderboard for solo players and one for teams. Also, players can only review neutralizations that are NOT from their team members.",
        Token.TUTO_END: "That's it! You are now ready to play. If that's your first time here, we'll ask a couple of questions to get you started.",


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
        
        # Messages
        Token.UNKNOWN_COMMAND: "Sorry, I didn't understand that command.",
        Token.DEFAULT_GREETING: "Hi there! How can I assist you today?",
        Token.DEFAULT_UNKNOWN: "I'm not sure how to respond to that. Try using /help.",
        Token.ASK_LANGUAGE: "Hello! I need to ask you a few questions to get started. What is your working language?",
        Token.ASK_IF_IN_TEAM: "Are you in a team?",
        Token.ASK_TEAM: "What is your team?",
        Token.ASK_ROLE: "What is your role?",
        Token.FINISH_ONBOARDING: "Thank you! You are all set!",
        Token.START_EXISTING_USER: "Welcome back! Use /play to start playing!",
        Token.START_NEW_USER: "Welcome to the game, let's start with a few questions!",

        Token.MAIN_MENU_INTRO: "Click one of the following commands to navigate the game:",
        Token.MAIN_MENU_PLAY: "/play to start playing",
        Token.MAIN_MENU_HELP: "/help for assistance",
        Token.MAIN_MENU_END_GAME: "/end to end the game",
        Token.MAIN_MENU_LEADERBOARD: "/leaderboard to show the leaderboard",

        Token.NOTHING_TO_DO: "You have nothing to do at the moment.",
        Token.NEUTRALIZE_THIS: "Please neutralize the following segment. Type a gender-agnostic alternative or copy-paste the original sentence if it's good to go.",
        Token.REVIEW_THIS: "Please review the following neutralization. Copy and paste in the chat the one you think is the best and send it.",
        Token.SUCCESSFUL_NEW_NEUTRALIZATION: "Your neutralization has been successfully submitted.",
        Token.SUCCESSFUL_NEW_REVIEW: "Your review has been successfully submitted.",
        Token.COULD_NOT_SAVE_SUBMISSION: "Your submission encountered an error.",

        Token.LIMIT_REACHED: "You have reached the limit of participations for today. You will be able to play again starting midnight. See you tomorrow!",
    },
    'fr': {
        Token.OK: 'OK',
        Token.YES: 'Oui',
        Token.NO: 'Non',

        Token.TUTO_INTRO: "Bienvenue dans le tutoriel du jeu ! Ici, vous apprendrez comment jouer.",
        Token.TUTO_GAME_GOAL: "Le but du jeu est de rendre les traductions de jeux vidéo neutres en termes de genre. Cela signifie que les phrases ne doivent pas avoir de marqueur de genre. C'est ce que nous appelons la 'Neutralisation'.",
        Token.TUTO_ROLES: "Pour améliorer la qualité des soumissions, il y a deux rôles dans le jeu : Neutralisaire et Révisaire. Les Neutralisaires sont responsables de la neutralisation du texte, tandis que les Révisaires sont responsables de la révision des neutralisations.",
        Token.TUTO_NEUTRALIZER: "Les Neutralisaires sont responsables de la neutralisation du texte. Si vous êtes un neutralisaire, votre objectif est de fournir la meilleure alternative de traduction neutre en termes de genre. Il vous suffit de la taper dans le chat et de l'envoyer. Si le segment ne nécessite aucune modification, copiez-collez le segment original dans le chat et envoyez-le.",
        Token.TUTO_REVIEWER: "Les Révisaires sont responsables de la révision des neutralisations. Si vous êtes révisaire, votre objectif est de choisir les meilleures neutralisations de la liste qui vous sera donnée. Il vous suffit de copier-coller celle que vous pensez être la meilleure dans le chat et de l'envoyer.",
        Token.TUTO_HYBRID: "En plus des neutralisaires et des révisaires, il est également possible d'être hybride. Cela signifie jouer les deux rôles en même temps : ce rôle se verra attribuer une neutralisation ou une révision au hasard. Cependant, il n'est pas possible de réviser ses propres neutralisations.",
        Token.TUTO_LEADERBOARD: "Le classement montre les scores. La neutralisation et la révision accordent toujours des points. Si vous êtes neutralisaire, des points bonus sont accordés si votre neutralisation a été choisie le plus souvent par les révisaires. Si vous êtes révisaire, des points bonus sont accordés si votre révision a été la plus choisie par les autres révisaires.",
        Token.TUTO_STREAK: "Chaque jour, vous recevrez une notification Telegram pour venir jouer. Si vous jouez plusieurs jours d'affilée, vous obtiendrez un bonus de série. Plus la série est longue, plus le bonus est important.", 
        Token.TUTO_TEAM: "Vous pouvez faire partie d'une équipe (ou choisir de jouer en solo). Il y a un classement pour les équipes, et un autre si vous jouez en solo. De plus, les révisaires ne peuvent réviser que les neutralisations qui n'ont PAS été faites par leurs coéquipiers.",
        Token.TUTO_END: "C'est tout ! Vous pouvez maintenant jouer. Si c'est votre première connexion, nous allons simplement vous poser quelques questions avant de commencer.",

        Token.FRENCH: 'Français',
        Token.ENGLISH: 'Anglais',

        Token.WELCOME: 'Bienvenue !',
        Token.PLAY_BUTTON: 'Jouer',
        Token.HELP_BUTTON: 'Aide',
        Token.END_GAME_BUTTON: 'Terminer le jeu',
        Token.SHOW_SCORE_BUTTON: 'Afficher le score',
        Token.NEUTRALIZER_ROLE: 'Neutralisaire',
        Token.REVIEWER_ROLE: 'Révisaire',
        Token.HYBRID_ROLE: 'Hybride',
        Token.TODAYS_MWE: "MWE d'aujourd'hui",
        Token.SUBMIT: 'Soumettre',
        Token.REVIEW: 'Réviser',
        Token.CHANGE_LANGUAGE: 'Changer de langue',

        # Messages
        Token.UNKNOWN_COMMAND: "Désolé, je n'ai pas compris cette commande.",
        Token.DEFAULT_GREETING: "Bonjour ! Comment puis-je t'aider aujourd'hui ?",
        Token.DEFAULT_UNKNOWN: "Je ne sais pas comment répondre à cela. Essaye d'utiliser /help.",
        Token.ASK_LANGUAGE: "Bonjour ! Je dois te poser quelques questions pour commencer. Quelle est ta langue de travail ?",
        Token.ASK_IF_IN_TEAM: "Es-tu dans une équipe ?",
        Token.ASK_TEAM: "Quelle est ton équipe ?",
        Token.ASK_ROLE: "Quel est ton rôle ?",
        Token.FINISH_ONBOARDING: "Merci ! Que le jeu commence !",
        Token.START_EXISTING_USER: "Bon retour ! Utilise /play pour commencer à jouer !",
        Token.START_NEW_USER: "Bienvenue dans le jeu, commençons par quelques questions !",

        Token.MAIN_MENU_INTRO: "Clique sur l'une des commandes suivantes pour naviguer dans le jeu :",
        Token.MAIN_MENU_PLAY: "/play pour commencer à jouer",
        Token.MAIN_MENU_HELP: "/help pour obtenir de l'aide",
        Token.MAIN_MENU_END_GAME: "/end pour terminer le jeu",
        Token.MAIN_MENU_LEADERBOARD: "/leaderboard pour afficher le classement",

        Token.NOTHING_TO_DO: "Tu n'as rien à faire pour le moment.",
        Token.NEUTRALIZE_THIS:  "Neutralise le segment suivant. Dans le chat, propose une alternative non-genrée ou copie-colle la phrase intiale si elle est déjà neutre.",
        Token.REVIEW_THIS: "Révise la neutralisation suivante. Copie-colle dans le chat celle que tu penses être la meilleure avant de l'envoyer.",
        Token.SUCCESSFUL_NEW_NEUTRALIZATION: "Ta neutralisation a été enregistrée avec succès.",
        Token.SUCCESSFUL_NEW_REVIEW: "Ta révision a été enregistrée avec succès.",
        Token.COULD_NOT_SAVE_SUBMISSION: "Ton entrée a rencontré une erreur.",

        Token.LIMIT_REACHED: "Tu as atteint la limite de participations pour aujourd'hui. Tu pourras de nouveau jouer à partir de minuit. À demain !"
    }
}
