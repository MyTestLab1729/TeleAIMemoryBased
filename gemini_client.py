import requests
import json
from config import GEMENI_API_KEY

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMENI_API_KEY}"

def convert_to_gemini_format(history):
    return {
        "contents": [
            {
                "role": m["role"],  # must be "user" or "model"
                "parts": [{"text": m["content"]}]
            }
            for m in history
        ]
    }

def get_gemini_response(history):
    headers = {"Content-Type": "application/json"}
    payload = convert_to_gemini_format(history)

    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Failed to parse response from Gemini."
    else:
        return f"Error {response.status_code}: {response.text}"
