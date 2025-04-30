import requests
import json
import base64
from config import GEMENI_API_KEY

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={GEMENI_API_KEY}"

def generate_image(prompt):
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_json = response.json()
        for candidate in response_json.get('candidates', []):
            for part in candidate.get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    image_base64 = part['inlineData']['data']
                    image_data = base64.b64decode(image_base64)
                    image_path = 'generated_image.png'
                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_data)
                    return image_path
        raise ValueError("No image data found in the response.")
    else:
        raise RuntimeError(f"Request failed with status code {response.status_code}: {response.text}")