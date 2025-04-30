import google.generativeai as genai
from config import GEMENI_API_KEY

genai.configure(api_key=GEMENI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def convert_to_gemini_format(history):
    return [
        {
            "role": m["role"],
            "parts": [{"text": m["content"]}]
        }
        for m in history
    ]

def get_gemini_response(history):
    formatted = convert_to_gemini_format(history)
    response = model.generate_content(formatted)
    return response.text
