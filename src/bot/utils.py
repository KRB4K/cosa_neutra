from telegram import Update
from telegram import Chat, Message, User
from telegram.ext import ContextTypes


from api.main import load_active_user
from api import models
import db
from static import DEFAULT_GAME
from states import get_current_lang, set_current_lang

def get_entities(update: Update) -> tuple[Chat, Message, User]:
    chat: Chat = update.effective_chat
    message: Message = update.effective_message
    user: User = update.effective_user
    return chat, message, user


async def _reset():
    pierre = 6384730936
    await models.User.ax_coll.delete_one({'id':pierre})
    await db.ASYNC.team_members.delete_one({
            "player":pierre,
            "game": DEFAULT_GAME
        })
    

def add_lang_to_context(function):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not get_current_lang(context):
            user = await load_active_user(update, context)
            set_current_lang(context, user.working_language)
        return await function(update, context)
    return wrapper