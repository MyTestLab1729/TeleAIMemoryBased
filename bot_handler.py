# --- bot_handler.py ---
from db_manager import get_history, add_message, clear_history
from gemini_client import get_gemini_response
from config import MAX_TOKENS
from utils import count_tokens, trim_history

def handle_messages(bot, message):
    chat_id = str(message.chat.id)
    user_text = message.text.strip()

    if user_text.lower() == "/clear_history":
        clear_history(chat_id)
        bot.reply_to(message, "Your history has been cleared.")
        return

    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})

    # Trim if over token limit
    if count_tokens(history) > MAX_TOKENS:
        history = trim_history(history, MAX_TOKENS)

    reply = get_gemini_response(history)
    history.append({"role": "model", "content": reply})

    add_message(chat_id, {"role": "user", "content": user_text})
    add_message(chat_id, {"role": "model", "content": reply})

    bot.reply_to(message, reply)