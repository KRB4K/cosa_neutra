import httpx
from telegram import Chat

from settings import BOT_TOKEN, TELEGRAM_API


async def get(url, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, *args, **kwargs)
        return response.json()
    
async def post(url: str, data: dict, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, *args, **kwargs)
        return response.json()  

async def send_notification(chat: Chat, message:str):
    url = TELEGRAM_API + f'/bot{BOT_TOKEN}/sendMessage'
    # message = urllib.parse.quote_plus(message)
    params = {
        'chat_id':chat.id,
    }
    body = {
        'text':message
    }
    response = await post(url, body, params=params)
    return response