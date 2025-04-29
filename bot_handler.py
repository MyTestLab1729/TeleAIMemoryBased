# --- bot_handler.py ---
import os  # Import the os module for file deletion
from db_manager import get_history, add_message, clear_history
from gemini_client import get_gemini_response
from config import MAX_TOKENS
from utils import count_tokens, trim_history
from text_to_image import generate_image  # Import the image generation function
import time  # Import time for simulating delays

# Default instruction to prepend to user prompts
DEFAULT_PROMPT = (
    "Always reply in the user's language. And act as a girlfriend/boyfriend according to the user's preferences. "
    "Make your responses compatible with Telegram by using emojis, "
    "bullet points, and formatting to make the response attractive and engaging."
    "Don't reply like a robot prepending the predefined instruction. "
    "Instead, use the instruction to guide your response and make it more engaging. "
    "Answer in short if user not specifies for long answer. "
    "Don't use the instruction in your response and add any meta-data give reponse directly. "
)

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
            # Indicate that the bot is generating an image
            bot.send_chat_action(chat_id, "upload_photo")
            time.sleep(1)  # Simulate a short delay for better UX

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