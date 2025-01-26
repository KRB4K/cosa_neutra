
from telegram import Update
from telegram.ext import CallbackContext
from api.models import User, UserWithRole, Neutralizer, Reviewer, Hybrid

async def load_active_user(update: Update, context: CallbackContext) -> User|UserWithRole:
    id = update.effective_user.id
    user = User.from_id(id)
    if user and user.role:
        user = user.to_role()
    return user