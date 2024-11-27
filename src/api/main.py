
from telegram import Update
from telegram.ext import CallbackContext
from api.models import User

async def load_active_user(update: Update, context: CallbackContext) -> User:
    id = update.effective_user.id
    return User.from_id(id)