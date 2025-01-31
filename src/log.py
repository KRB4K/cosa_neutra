import logging
import os
from logging.handlers import RotatingFileHandler

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
console_handler = logging.StreamHandler()
# Determine the top level directory of the repo
top_level_dir = os.path.dirname(os.path.abspath(__file__))

# Create the logs directory if it doesn't exist
logs_dir = os.path.join(top_level_dir, 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Define the rotating file handler with a relative path
file_handler = RotatingFileHandler(
    os.path.join(logs_dir, 'logfile.log'), maxBytes=1024*1024, backupCount=10
)

# Set level for handlers
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Suppress warnings from specific libraries
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("telegram.ext._application").setLevel(logging.DEBUG)