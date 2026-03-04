import os
import logging
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
                    format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

if TELEGRAM_TOKEN is None:
    logger.warning('TELEGRAM_TOKEN is not set. Create a .env file based on .env.example')

# Helper: safe owner check (compare as strings)
def is_owner(user_id):
    if OWNER_ID is None:
        return False
    return str(user_id) == str(OWNER_ID)
