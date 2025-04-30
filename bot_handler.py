# --- bot_handler.py ---
import os
from db_manager import get_history, add_message, clear_history
from gemini_client import get_gemini_response
from config import MAX_TOKENS
from utils import count_tokens, trim_history
from text_to_image import generate_image  # Updated to handle both text and image
import time

# Default instruction to prepend to user prompts
DEFAULT_PROMPT = ""
with open("DefaultPrompt.txt", "r") as f:
    DEFAULT_PROMPT = f.read().strip()

# Dictionary to track user states
user_states = {}

def handle_messages(bot, message):
    chat_id = str(message.chat.id)
    user_text = message.text.strip()

    # Check if the user is in the middle of an /imagine interaction
    if user_states.get(chat_id) == "awaiting_imagine_prompt":
        # Process the user's response to the /imagine command
        try:
            bot.send_chat_action(chat_id, "upload_photo")
            time.sleep(1)  # Simulate a short delay for better UX

            # Generate content (text and/or image)
            image_path = generate_image(user_text)

            # Send image response if available
            if image_path:
                with open(image_path, "rb") as image_file:
                    bot.send_photo(chat_id, image_file)
                os.remove(image_path)  # Delete the image after sending

        except Exception as e:
            bot.reply_to(message, f"Failed to generate content: {str(e)}")

        # Reset the user's state
        user_states.pop(chat_id, None)
        return

    # Handle the /imagine command
    if user_text.lower() == "/imagine":
        # Set the user's state to awaiting an imagine prompt
        user_states[chat_id] = "awaiting_imagine_prompt"
        bot.reply_to(message, "What do you want to imagine?")
        return

    # Handle the /clear_history command
    if user_text.lower() == "/clear_history":
        clear_history(chat_id)
        bot.reply_to(message, "Your history has been cleared.")
        return

    # Handle normal text prompts (Gemini text response)
    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})

    # Create a temporary prompt with the default instruction
    full_prompt = f"{DEFAULT_PROMPT}\n\n{user_text}"

    # Trim history if it exceeds the token limit
    if count_tokens(history) > MAX_TOKENS:
        history = trim_history(history, MAX_TOKENS)

    # Indicate that the bot is typing
    bot.send_chat_action(chat_id, "typing")
    time.sleep(1)  # Simulate a short delay for better UX

    # Send the modified prompt to Gemini without altering the history
    temp_history = history[:-1] + [{"role": "user", "content": full_prompt}]
    reply = get_gemini_response(temp_history)

    # Add the user's original input and Gemini's reply to the history
    history.append({"role": "model", "content": reply})

    # Save the conversation history
    add_message(chat_id, {"role": "user", "content": user_text})
    add_message(chat_id, {"role": "model", "content": reply})

    # Send the reply to the user
    bot.reply_to(message, reply)