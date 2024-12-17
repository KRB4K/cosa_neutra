from telegram import Update
from telegram import Chat, Message, User

from api import models
import db
from static import DEFAULT_GAME

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