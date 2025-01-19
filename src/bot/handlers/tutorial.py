
from telegram import Update
from telegram.ext import CallbackContext

import keyboards
from locales import translate, Token
from states import State, set_state


async def intro(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_INTRO, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_INTRO_SENT)

async def game_goal(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_GAME_GOAL, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_GAME_GOAL_SENT)

async def tuto_roles(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_ROLES, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_ROLES_SENT)

async def tuto_neutralizer(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_NEUTRALIZER, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_NEUTRALIZER_SENT)

async def tuto_reviewer(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_REVIEWER, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_REVIEWER_SENT)

async def tuto_hybrid(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_HYBRID, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_HYBRID_SENT)

async def tuto_leaderboard(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_LEADERBOARD, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_LEADERBOARD_SENT)

async def tuto_streak(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_STREAK, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_STREAK_SENT)

async def tuto_team(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_TEAM, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_TEAM_SENT)

async def tuto_end(update: Update, context: CallbackContext):
    reply = translate(Token.TUTO_END, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
        reply_markup=keyboards.ok(context)
    )
    set_state(context, State.TUTO_END_SENT)



