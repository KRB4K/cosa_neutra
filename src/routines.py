import aiocron
import asyncio
import api.models as models
from connect import send_notification
from locales import Token, translate

async def send_play_notification():
    active_users = models.UserWithRole.get_all_active_users()
    for user in active_users:
        await send_notification(user.chat_id, translate(Token.COME_PLAY, context=None, lang=user.working_language))


aiocron.crontab('0 9 * * *', func=send_play_notification)

aiocron.crontab('0 1 * * *', func=models.Segment.update_segment_winners)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever()