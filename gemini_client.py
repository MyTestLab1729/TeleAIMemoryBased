#  Termux Version:
# import requests
# import json
# from config import GEMENI_API_KEY

# GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMENI_API_KEY}"

# def convert_to_gemini_format(history):
#     return {
#         "contents": [
#             {
#                 "role": m["role"],  # must be "user" or "model"
#                 "parts": [{"text": m["content"]}]
#             }
#             for m in history
#         ]
#     }

# def get_gemini_response(history):
#     headers = {"Content-Type": "application/json"}
#     payload = convert_to_gemini_format(history)

#     response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))

#     if response.status_code == 200:
#         result = response.json()
#         try:
#             return result['candidates'][0]['content']['parts'][0]['text']
#         except (KeyError, IndexError):
#             return "Failed to parse response from Gemini."
#     else:
#         return f"Error {response.status_code}: {response.text}"

# EC2 Version:
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