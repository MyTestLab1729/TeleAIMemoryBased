# --- gemini_client.py ---
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(history):
    response = model.generate_content(history)
    return response.text