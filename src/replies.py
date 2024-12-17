from locales import translate, Token

def main_menu(update, context):
    message = f"""{translate(Token.MAIN_MENU_INTRO, update)}
- {translate(Token.MAIN_MENU_PLAY, update)}
- {translate(Token.MAIN_MENU_LEADERBOARD, update)}
- {translate(Token.MAIN_MENU_HELP, update)}"""
    return message
