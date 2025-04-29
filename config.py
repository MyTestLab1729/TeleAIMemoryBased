# --- config.py ---
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
GEMINI_API_KEY = "your_gemini_api_key"
DB_PATH = "chat_history.db"
MAX_TOKENS = 12000  # Trim if history exceeds this

# --- main.py ---
from telebot import TeleBot
from config import TELEGRAM_BOT_TOKEN
from bot_handler import handle_messages

bot = TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def message_handler(message):
    handle_messages(bot, message)

print("Bot is running...")
bot.infinity_polling()