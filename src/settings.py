import os
import dotenv

dotenv.load_dotenv()
BOT_TOKEN: str = os.getenv('telegram_bot_token')
DB_NAME: str = os.getenv('db_name')
GAME_NAME: str = os.getenv('game_name')