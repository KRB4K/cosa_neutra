import os
import logging
import urllib
import urllib.parse
import httpx

import dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppress warnings from HTTP library
logging.getLogger("telegram.ext._application").setLevel(logging.WARNING)  # Adjust specific Telegram logger

dotenv.load_dotenv()
BOT_TOKEN: str = os.getenv('telegram_bot_token')
GAME_NAME: str = os.getenv('game_name')
assert all((BOT_TOKEN, GAME_NAME)), 'Envrionment variables missing'

TG_API = 'https://api.telegram.org'

user_states = {}
PLAY, END, LANGUAGE, TEAM, ROLE = range(5)



main_menu_keyboard = [
    [KeyboardButton('Play'), KeyboardButton('Help')],
    [KeyboardButton('End Game'), KeyboardButton('Show Score')]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True, one_time_keyboard=True)

role_keyboard = [
    [KeyboardButton('Neutralizer'), KeyboardButton('Reviewer')],
    [KeyboardButton('Hybrid')]
]
role_markup = ReplyKeyboardMarkup(role_keyboard, resize_keyboard=True, one_time_keyboard=True)

# async def get_active_user(user: User) -> User|None:

async def get(url, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, *args, **kwargs)
        return response.json()
    
async def post(url: str, data: dict, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, *args, **kwargs)
        return response.json()  

async def send_notification(chat: Chat, message:str):
    url = TG_API + f'/bot{BOT_TOKEN}/sendMessage'
    # message = urllib.parse.quote_plus(message)
    params = {
        'chat_id':chat.id,
    }
    body = {
        'text':message
    }
    response = await post(url, body, params=params)
    return response

def get_entities(update: Update) -> tuple[Chat, Message, User]:
    chat: Chat = update.effective_chat
    message: Message = update.effective_message
    user: User = update.effective_user
    return chat, message, user

async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.") # type: ignore

async def default_handler(update: Update, context: CallbackContext) -> None:
    """Handler for any non-command messages."""
    user_message = update.message.text
    logger.info(f"Received message: {user_message} from user: {update.effective_user.id}")

    # Here you can parse the input or trigger other kinds of actions
    if "hello" in user_message.lower():
        await update.message.reply_text("Hi there! How can I assist you today?")
    else:
        await update.message.reply_text("I'm not sure how to respond to that. Try using /help.")


async def ask_language(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's working language."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I need to ask you a few questions to get started. What is your working language?"
    )
    return LANGUAGE

async def ask_team(update: Update, context: CallbackContext) -> int:
    """Handler to ask if the user has a team."""
    user_id = update.effective_user.id
    user_states[user_id] = {"language": update.message.text}
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Do you have a team? If so, which one?"
    )
    return TEAM

async def ask_role(update: Update, context: CallbackContext) -> int:
    """Handler to ask for the user's role."""
    user_id = update.effective_user.id
    user_states[user_id]["team"] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What is your role?",
        reply_markup=role_markup
    )
    return ROLE

async def finish_onboarding(update: Update, context: CallbackContext) -> int:
    """Handler to finish onboarding process."""
    user_id = update.effective_user.id
    user_states[user_id]["role"] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Thank you! You are all set. Use /play to start playing!",
        reply_markup=main_menu_markup
    )
    return ConversationHandler.END



# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat, message, user = get_entities(update)
#     user: User = update.effective_user
#     text = f'Welcome to {GAME_NAME}, {user.first_name}!'
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id, # type: ignore
#         text=text,
#         reply_markup=main_menu_markup
#         )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handler for /start command."""
    user_id = update.effective_user.id
    if user_id not in user_states:
        logger.info(f"User {user_id} is new. Starting onboarding process.")
        return await ask_language(update, context)
    
    logger.info(f"User {user_id} has started the bot.")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome back! Use /play to start playing!",
        reply_markup=main_menu_markup
    )
    return ConversationHandler.END

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))

    application.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, default_handler))
    
    application.run_polling()