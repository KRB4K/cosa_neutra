from re import S
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from log import logger

from locales import translate, Token


async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=translate(Token.UNKNOWN_COMMAND, update)) # type: ignore

async def default_handler(update: Update, context: CallbackContext) -> None:
    """Handler for any non-command messages."""
    await update.message.reply_text(translate(Token.DEFAULT_UNKNOWN, update)) # type: ignore


