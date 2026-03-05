import os
import requests
from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv('PRODUCTION', 'false') == 'true'
HF_TOKEN = os.getenv('HF_TOKEN', '')

if PRODUCTION:
    def get_embedding(text):
        API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        return response.json()
else:
    import random
    def get_embedding(text):
        print(f"[DEV] Fake embedding for: {text}")
        return [random.uniform(-1, 1) for _ in range(384)]
