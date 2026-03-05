import os
from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv('PRODUCTION', 'false') == 'true'

if PRODUCTION:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    def get_embedding(text):
        return model.encode(text).tolist()
else:
    import random
    def get_embedding(text):
        print(f"[DEV] Fake embedding for: {text}")
        return [random.uniform(-1, 1) for _ in range(384)]