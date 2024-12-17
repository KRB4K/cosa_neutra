from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from log import logger

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


