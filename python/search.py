from pymongo import MongoClient
from embeddings import get_embedding
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]

def semantic_search(query, top_k=5):
    query_embedding = get_embedding(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 20,
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
    ])
    return list(results)


def keyword_search(query, top_k=5):
    results = collection.aggregate([
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
    ])
    return list(results)


def hybrid_search(query, top_k=3):
    semantic_results = semantic_search(query, top_k=5)
    keyword_results = keyword_search(query, top_k=5)

    rrf_scores = {}

    for rank, doc in enumerate(semantic_results):
        text = doc['text']
        rrf_scores[text] = rrf_scores.get(text, 0) + 1 / (rank + 1 + 60)

    for rank, doc in enumerate(keyword_results):
        text = doc['text']
        rrf_scores[text] = rrf_scores.get(text, 0) + 1 / (rank + 1 + 60)

    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    return [{"text": text, "score": round(score, 6)} for text, score in ranked[:top_k]]
