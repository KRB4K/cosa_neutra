import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppress warnings from HTTP library
logging.getLogger("telegram.ext._application").setLevel(logging.WARNING)  # Adjust specific Telegram logger