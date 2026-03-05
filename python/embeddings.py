import os
import random
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()


def _env_to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


PRODUCTION = _env_to_bool(os.getenv("PRODUCTION", "false"))
HF_TOKEN = os.getenv("HF_TOKEN", "")
MODEL_DIMENSION = 384


def _normalize_embedding(result) -> List[float]:
    """
    Normalize Hugging Face API responses into a single 1D embedding vector.

    Supported common shapes:
    - [dim]
    - [[dim]]
    - [[seq_len x dim]]
    """
    if not isinstance(result, list) or not result:
        raise RuntimeError(f"Invalid embedding payload received: {result}")

    first = result[0]

    # [dim]
    if isinstance(first, (int, float)):
        return [float(x) for x in result]

    # [[dim]]
    if isinstance(first, list) and first and isinstance(first[0], (int, float)):
        return [float(x) for x in first]

    # [[seq_len x dim]] -> mean pool token embeddings
    if (
        isinstance(first, list)
        and first
        and isinstance(first[0], list)
        and first[0]
        and isinstance(first[0][0], (int, float))
    ):
        token_vectors = first
        dim = len(token_vectors[0])
        pooled = [0.0] * dim
        for token in token_vectors:
            for i, val in enumerate(token):
                pooled[i] += float(val)
        return [v / len(token_vectors) for v in pooled]

    raise RuntimeError(f"Unsupported embedding response shape: {type(result)}")


if PRODUCTION:
    def get_embedding(text: str) -> List[float]:
        api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": text, "options": {"wait_for_model": True}},
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and result.get("error"):
            raise RuntimeError(f"Hugging Face API error: {result['error']}")

        embedding = _normalize_embedding(result)

        if len(embedding) != MODEL_DIMENSION:
            raise RuntimeError(
                f"Unexpected embedding dimension {len(embedding)} (expected {MODEL_DIMENSION})."
            )

        return embedding
else:
    def get_embedding(text: str) -> List[float]:
        print(f"[DEV] Fake embedding for: {text}")
        return [random.uniform(-1, 1) for _ in range(MODEL_DIMENSION)]
