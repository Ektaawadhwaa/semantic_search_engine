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
                "_id": 1,
                "text": 1,
                "category": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    return list(collection.aggregate(pipeline))#execute query


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
                "_id": 1,
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

    scores = {}
    doc_map = {}
    for doc in semantic_results:
        _id = str(doc["_id"])
        scores[_id] = scores.get(_id, 0) + doc["score"] * 0.7
        doc_map[_id] = doc
    max_kw = max((d["score"] for d in keyword_results), default=1)
    for doc in keyword_results:
        _id = str(doc["_id"])
        scores[_id] = scores.get(_id, 0) + (doc["score"] / max_kw) * 0.3
        doc_map[_id] = doc
     

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #Sorts documents by score.
 
    return [
    {
        "text": doc_map[_id]["text"],
        "category": doc_map[_id].get("category", "general"),
        "score": round(score, 4)
    }
    for _id, score in ranked[:top_k]
]