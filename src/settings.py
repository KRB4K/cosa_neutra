import os
import dotenv

dotenv.load_dotenv()
BOT_TOKEN: str = os.getenv('telegram_bot_token')
DB_NAME: str = os.getenv('db_name')
GAME_NAME: str = os.getenv('game_name')
MONGO_URI: str = os.getenv('mongo_uri')

TELEGRAM_API = 'https://api.telegram.org'

DAILY_NEUTRALIZATIONS = 5
DAILY_REVIEWS = 5