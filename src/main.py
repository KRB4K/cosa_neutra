
from telegram import Update
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler

from bot.handlers.fallbacks import unknown_command_handler, default_handler
from bot.handlers.main import message_handler
from bot.handlers.start import start_handler
from bot.handlers.play import submit
from bot.handlers.tutorial import intro
from settings import BOT_TOKEN, GAME_NAME

assert all((BOT_TOKEN, GAME_NAME)), 'Envrionment variables missing'


if __name__ == '__main__':

    
    application = ApplicationBuilder()\
        .token(BOT_TOKEN)\
        .build()

    
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('play', submit))
    application.add_handler(CommandHandler('help', intro))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
    
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
