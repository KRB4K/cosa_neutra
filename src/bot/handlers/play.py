import logging
import random

from bson import ObjectId
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import Chat, Message, User
from telegram.ext import filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

from api.main import load_active_user
import api.models as models
import api.enums
import db
import keyboards
import replies
from static import WORKING_LANGUAGES, DEFAULT_GAME
import states
from locales import translate, get_user_language, TRANSLATIONS, Token

async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_user: models.UserWithRole = await load_active_user(update, context)
    assert isinstance(active_user, models.UserWithRole)

    to_do = active_user.next_to_do()  # default value for None
    data = to_do.get("data")
    if not data:
        reply = translate(Token.NOTHING_TO_DO, context)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply
        )
        return

    task = to_do['task']
    to_do_id = f'{task}_{to_do["segment"]}'
    reply = ''
    match task:

        case 'neutralization':
            reply += translate(Token.NEUTRALIZE_THIS, context)
            reply += '\n\n\n'
            reply += f'<b>{data}</b>'
            
        case 'review':
            reply += translate(Token.REVIEW_THIS, context)
            reply += '\n\n\n'
            data = [f'<b>{d}</b>' if i % 2 == 0 else f'<i>{d}</i>' for i, d in enumerate(data)]
            reply += '\n\n'.join(data)

    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        parse_mode='HTML'
    )
    states.set_current_to_do(context, to_do_id)
    states.set_state(context, states.State.HAS_ONGOING_TASK)
    return
        

async def register_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_user: models.UserWithRole = await load_active_user(update, context)
    assert isinstance(active_user, models.UserWithRole)

    to_do = states.get_current_to_do(context)
    type, id = to_do.split('_')
    oid = ObjectId(id)

    match type:

        case 'neutralization':
            text = update.message.text
            neutralization = models.Neutralization.insert(
                segment=oid,
                text=text,
                by=active_user
            )
            if neutralization:
                reply = translate(Token.SUCCESSFUL_NEW_NEUTRALIZATION, context)
                
            else:
                reply = translate(Token.COULD_NOT_SAVE_SUBMISSION, context)
                
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply
            )

            states.clear_current_to_do(context)
            states.clear_state(context)


        case 'review':
            text = update.message.text.strip()
            neutralization = models.Neutralization.from_oid(oid)
            if not neutralization:
                reply = translate(Token.COULD_NOT_SAVE_SUBMISSION, context)
            else:
                approved = text == neutralization.text
                review = models.Review.insert(
                    neutralization=neutralization,
                    text=text,
                    approved=approved,
                    by=active_user
                )
                if review:
                    reply = translate(Token.SUCCESSFUL_NEW_REVIEW, context)
                else:
                    reply = translate(Token.COULD_NOT_SAVE_SUBMISSION, context)
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply
            )
            states.clear_current_to_do(context)
            states.clear_state(context)
        
    states.clear_current_to_do(context)
    states.set_state(context, states.State.NONE)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies.main_menu(update, context)
    )
    return

    
        
    