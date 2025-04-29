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