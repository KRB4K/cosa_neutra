
from telegram import Update
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, PicklePersistence, ContextTypes

from bot.handlers.main import unknown_command_handler, default_handler
from bot.handlers.message import message_handler
from bot.handlers.start import start_handler
from settings import BOT_TOKEN, GAME_NAME

assert all((BOT_TOKEN, GAME_NAME)), 'Envrionment variables missing'

    # await update.callback_query.edit_message_text(text="Selected option: {}".format(update.callback_query.data))

from telegram.ext import CallbackQueryHandler

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query


    # CallbackQueries need to be answered, even if no notification to the user is needed

    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    await query.answer()


    await query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == '__main__':
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    # application = ApplicationBuilder()\
    #     .token(BOT_TOKEN)\
    #     .persistence(persistence)\
    #     .arbitrary_callback_data(True)\
    #     .build()
    
    application = ApplicationBuilder()\
        .token(BOT_TOKEN)\
        .build()

    
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(CallbackQueryHandler(message_handler))
    # application.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))
    
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
