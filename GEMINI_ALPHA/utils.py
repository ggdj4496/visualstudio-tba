import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    OWNER_ID = int(os.getenv('OWNER_ID', '5972265370'))
    BASE_DIR = r'C:\visualstudio tba\GEMINI_ALPHA'

def is_owner(user_id):
    return user_id == Config.OWNER_ID

logging.basicConfig(level=logging.INFO, format='[SIGMA] %(message)s')
logger = logging.getLogger('SIGMA')