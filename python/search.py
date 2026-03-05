from pymongo import MongoClient
from embeddings import get_embedding
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

if not all([MONGO_URI, DB_NAME, COLLECTION_NAME]):
    raise ValueError("Missing MongoDB environment variables")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def semantic_search(query, top_k=5):
    query_embedding = get_embedding(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 50,
                "limit": top_k
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "category": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def keyword_search(query, top_k=5):
    pipeline = [
        {
            "$search": {
                "index": "keyword_index",
                "text": {
                    "query": query,
                    "path": "text"
                }
            }
        },
        {"$limit": top_k},
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "category": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def hybrid_search(query, top_k=3):
    semantic_results = semantic_search(query, top_k=5)
    keyword_results = keyword_search(query, top_k=5)

    rrf_scores = {}
    doc_map = {}

    k = 60  # RRF constant

    for rank, doc in enumerate(semantic_results):
        key = doc['text']
        rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (rank + k)
        doc_map[key] = doc

    for rank, doc in enumerate(keyword_results):
        key = doc['text']
        rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (rank + k)
        doc_map[key] = doc

    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for text, score in ranked[:top_k]:
        doc = doc_map[text]
        results.append({
            "text": doc["text"],
            "category": doc.get("category"),
            "score": round(score, 6)
        })

    return results