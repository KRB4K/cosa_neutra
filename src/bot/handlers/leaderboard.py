from operator import ne
import re
import db
import api.models as models
from telegram.ext import ApplicationBuilder, ContextTypes
from utils import align_with_even_length

# f'{"Hi": <16} StackOverflow!'

def compute_leaderboard():
    users = models.UserWithRole.get_all_active_users()

    neutralizers = [(u, u.get_score().get('neutralization')) for u in users]
    neutralizers = filter(lambda x:x[1] != None, neutralizers)
    neutralizers = sorted(neutralizers, key=lambda x: x[1], reverse=True)  # type: ignore
    neutralizers = neutralizers[:10]
    neutralizers = [(u.first_name, s) for u, s in neutralizers]

    reviewers = [(u, u.get_score().get('review')) for u in users]
    reviewers = filter(lambda x:x[1] != None, reviewers)
    reviewers = sorted(reviewers, key=lambda x: x[1], reverse=True)  # type: ignore
    reviewers = reviewers[:10]
    reviewers = [(u.first_name, s) for u, s in reviewers]

    return neutralizers, reviewers

async def leaderboard(update, context: ContextTypes.DEFAULT_TYPE):
    neutralizers, reviewers = compute_leaderboard()

    neutralizers = '\n'.join([(align_with_even_length(str(score), name)) for name, score in neutralizers])
    reviewers = '\n'.join([(align_with_even_length(str(score), name)) for name, score in reviewers])

    reply = f'Neutralizers:\n{neutralizers}\n\nReviewers:\n{reviewers}'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply
    )



