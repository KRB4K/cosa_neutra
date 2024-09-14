import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('telegram_bot_token')
assert BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat)
    print(update.effective_message)
    print(update.effective_sender)
    print(update.effective_user)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, # type: ignore
        text="I'm a bot, please talk to me!"
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    
    application.run_polling()