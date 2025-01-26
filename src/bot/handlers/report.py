from datetime import datetime
from bson import ObjectId
import re
import db
from api.main import load_active_user
import api.models as models
from bot.handlers import play
from bot.utils import add_lang_to_context
from locales import translate, get_user_language, TRANSLATIONS, Token
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
import states
from utils import today


@add_lang_to_context
async def report_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply = translate(Token.WHAT_TO_REPORT, context)

    states.set_state(context, states.State.IS_REPORTING)


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply
    )


async def register_report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not (text := update.message.text.strip()):
        return translate(Token.REPORT_IS_MISSING, context)
    
    to_do = states.get_current_to_do(context)
    active_user = await load_active_user(update, context)

    type, id = to_do.split('_')
    oid = ObjectId(id)

    record = {
        'type': type,
        'segment': oid,
        'user': active_user.oid,
        'text': text,
        'created_at': datetime.now()
    }
    db.SYNC.reports.insert_one(record)

    states.clear_current_to_do(context)


    reply = translate(Token.REPORT_REGISTERED, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply
    )

    await play.submit(update, context)