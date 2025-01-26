
from bson import ObjectId
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

from api.main import load_active_user
import api.models as models
from bot.utils import add_lang_to_context
import replies
import states

from locales import translate, Token


@add_lang_to_context
async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_user: models.UserWithRole = await load_active_user(update, context)
    assert isinstance(active_user, models.UserWithRole)

    available_tasks = active_user.get_available_task_type()
    if not available_tasks:
        reply = translate(Token.LIMIT_REACHED, context)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply
        )
        return
    
    to_do = active_user.next_to_do(available_tasks)
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

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply,
                parse_mode='HTML'
            )
            
        case 'review':
            print(to_do)
            segment = models.Segment.from_oid(to_do['segment'])

            reply += translate(Token.ORIGINAL_SEGMENT, context)
            reply += '\n'
            reply += f'<blockquote>{segment.get_text_to_neutralize()}</blockquote>'
            reply += '\n\n\n'
            reply += translate(Token.REVIEW_THIS, context)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply,
                parse_mode='HTML'
            )

            for i, d in enumerate(data, start=1):
                reply = f'<b>N°{i}</b>'
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=reply,
                    parse_mode='HTML'
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=d,
                    # parse_mode='HTML'
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

    print('OID', oid)

    match type:

        case 'neutralization':
            text = update.message.text.strip()
            segment = models.Neutralization.insert(
                segment=oid,
                text=text,
                by=active_user
            )
            if segment:
                reply = translate(Token.SUCCESSFUL_NEW_NEUTRALIZATION, context)
                reply += f'<b>{text}</b>'
                
            else:
                reply = translate(Token.COULD_NOT_SAVE_SUBMISSION, context)
                
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply,
                parse_mode='HTML'
            )

            states.clear_current_to_do(context)
            states.clear_state(context)


        case 'review':
            text = update.message.text.strip()
        
            review = models.Review.insert(
                segment=oid,
                text=text,
                by=active_user
            )
            print('reviewed', review)
            if review:
                reply = translate(Token.SUCCESSFUL_NEW_REVIEW, context)
                reply += f'<b>{text}</b>'
            else:
                reply = translate(Token.COULD_NOT_SAVE_SUBMISSION, context)
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply,
                parse_mode='HTML'
            )
            states.clear_current_to_do(context)
            states.clear_state(context)

    print("clearing in register task")
    states.clear_current_to_do(context)
    states.set_state(context, states.State.NONE)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=replies.main_menu(update, context)
    )
    return

    
        
    