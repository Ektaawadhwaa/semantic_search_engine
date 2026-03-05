import os
import random
from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv("PRODUCTION", "false") == "true" 
if PRODUCTION:
    from sentence_transformers import SentenceTransformer

    print("Loading embedding model: all-MiniLM-L6-v2")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def get_embedding(text):
        embedding = model.encode(text)
        return embedding.tolist()

 

else:
    def get_embedding(text):
        print(f"[DEV] Fake embedding for: {text}")
        return [random.uniform(-1, 1) for _ in range(384)]