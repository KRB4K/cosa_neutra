
from telegram import Update
from telegram.ext import CallbackContext
from api.models import User, UserWithRole, Neutralizer, Reviewer, Hybrid

async def load_active_user(update: Update, context: CallbackContext) -> User|UserWithRole:
    id = update.effective_user.id
    user = User.from_id(id)
    if user and user.role:
        match user.role:
            case "neutralizer":
                user = Neutralizer.from_id(user.id)
            case "reviewer":
                user = Reviewer.from_id(user.id)
            case "hybrid":
                user = Hybrid.from_id(user.id)
    return user