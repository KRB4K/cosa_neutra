from locales import translate, Token

def main_menu(update, context):
    message = f"""{translate(Token.MAIN_MENU_INTRO, context)}
- {translate(Token.MAIN_MENU_PLAY, context)}
- {translate(Token.MAIN_MENU_LEADERBOARD, context)}
- {translate(Token.MAIN_MENU_HELP, context)}"""
    return message
