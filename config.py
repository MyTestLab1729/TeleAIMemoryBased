# --- config.py ---
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMENI_API_KEY = os.getenv("GEMENI_API_KEY")
DB_PATH = "chat_history.db"
MAX_TOKENS = 1048576  # Trim if history exceeds this
