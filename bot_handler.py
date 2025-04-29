# --- bot_handler.py ---
import os  # Import the os module for file deletion
from db_manager import get_history, add_message, clear_history
from gemini_client import get_gemini_response
from config import MAX_TOKENS
from utils import count_tokens, trim_history
from text_to_image import generate_image  # Import the image generation function

def handle_messages(bot, message):
    chat_id = str(message.chat.id)
    user_text = message.text.strip()

    # Handle the /clear_history command
    if user_text.lower() == "/clear_history":
        clear_history(chat_id)
        bot.reply_to(message, "Your history has been cleared.")
        return

    # Handle the /imagine command
    if user_text.lower().startswith("/imagine"):
        # Extract the prompt after the /imagine command
        prompt = user_text[len("/imagine"):].strip()
        if not prompt:
            bot.reply_to(message, "Please provide a prompt for the image generation.")
            return

        try:
            # Call the generate_image function to create the image
            image_path = generate_image(prompt)
            with open(image_path, "rb") as image_file:
                bot.send_photo(chat_id, image_file)
            # Delete the image after sending it
            os.remove(image_path)
        except Exception as e:
            bot.reply_to(message, f"Failed to generate image: {str(e)}")
        return  # Stop further processing for this command

    # Handle normal text prompts (Gemini text response)
    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})

    # Trim history if it exceeds the token limit
    if count_tokens(history) > MAX_TOKENS:
        history = trim_history(history, MAX_TOKENS)

    # Get the Gemini response
    reply = get_gemini_response(history)
    history.append({"role": "model", "content": reply})

    # Save the conversation history
    add_message(chat_id, {"role": "user", "content": user_text})
    add_message(chat_id, {"role": "model", "content": reply})

    # Send the reply to the user
    bot.reply_to(message, reply)