from telegram import Update
from telegram.ext import CallbackContext, ContextTypes


from api.main import load_active_user
from bot.handlers.fallbacks import default_handler
from bot.handlers import onboarding
from bot.utils import get_entities
from states import State, get_state, set_state, clear_state

from locales import get_user_language, translate, TRANSLATIONS


    

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    state = get_state(context)
    _, message, _ = get_entities(update)
    user = await load_active_user(update, context)
    user_lang = get_user_language(update)

    allowed_inputs = list(TRANSLATIONS[user_lang].values())

    if update.callback_query:
        callback_data = update.callback_query.data
        await update.callback_query.answer()
        print(f"Callback Data: {callback_data}")
    else:
        callback_data = None

    print(f"Callback Query: {update.callback_query}")
    print(f"Effective Chat: {update.effective_chat}")
    print(f"Effective Message: {update.effective_message}")
    print(f"Message: {update.message}")

    print('context', context)
    
    match state:
        case State.NONE:
            return await default_handler(update, context)
        
        case State.NEED_LANGUAGE:
            return await onboarding.ask_language(update, context)
        
        case State.LANGUAGE_IS_ASKED:
            if not message.text in allowed_inputs:
                raise ValueError("Invalid language")
            user.set_working_language(message.text)

            
            

    
    
