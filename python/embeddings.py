import os
import random
import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

PRODUCTION = os.getenv("PRODUCTION", "false") == "true"

# ---------------------------
# PRODUCTION MODE
# ---------------------------
if PRODUCTION:

    print("Loading embedding model: all-MiniLM-L6-v2")

    # load model once
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # force CPU (important for Render)
    model = model.to("cpu")

    def get_embedding(text: str):
        with torch.no_grad():
            embedding = model.encode(
                [text],                      # batch encoding
                convert_to_numpy=True,
                normalize_embeddings=True   # improves similarity search
            )[0]

        return embedding.tolist()


# ---------------------------
# DEVELOPMENT MODE
# ---------------------------
else:

    def get_embedding(text: str):
        print(f"[DEV] Fake embedding for: {text}")
        return [random.uniform(-1, 1) for _ in range(384)]