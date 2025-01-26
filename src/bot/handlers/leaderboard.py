from operator import add
import re
import db
import api.models as models
from bot.utils import add_lang_to_context
from locales import translate, get_user_language, TRANSLATIONS, Token
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

@add_lang_to_context
async def leaderboard(update, context: ContextTypes.DEFAULT_TYPE):
    neutralizers, reviewers = compute_leaderboard()

    neutralizers = '\n'.join([(align_with_even_length(str(score), name, n=5)) for name, score in neutralizers])
    reviewers = '\n'.join([(align_with_even_length(str(score), name, n=5)) for name, score in reviewers])

    neutralizers_reply = f'<b><u>{translate(Token.NEUTRALIZER_ROLE, context)}:</u></b>\n{neutralizers}'
    reviewers_reply = f'<b><u>{translate(Token.REVIEWER_ROLE, context)}:</u></b>:\n{reviewers}'

    # Team leaderboard
    teams = db.SYNC.teams.find({'active': True})
    teams = [models.Team.from_record(team) for team in teams]
    teams = [{'name': team.name, 'score': team.get_score()} for team in teams]
    teams = sorted(teams, key=lambda x: x['score'], reverse=True)
    teams = teams[:10]
    teams = [(team['name'], team['score']) for team in teams]
    teams = '\n'.join([(align_with_even_length(str(score), name, n=5)) for name, score in teams])

    team_reply = f'<b><u>{translate(Token.TEAM, context)}:</u></b>\n{teams}'

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=neutralizers_reply,
        parse_mode='HTML'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reviewers_reply,
        parse_mode='HTML'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=team_reply,
        parse_mode='HTML'
    )


