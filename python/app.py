from flask import Flask, request, jsonify
from flask_cors import CORS
from search import hybrid_search, collection
from embeddings import get_embedding
app = Flask(__name__)
CORS(app)
@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    text = data.get('text', '')
    category = data.get('category', 'general')
    date = data.get('date', '2024-01-01')

    if not text:
        return jsonify({"error": "text is required"}), 400

    # generate embedding
    embedding = get_embedding(text)

    # save to MongoDB
    doc = {
        "text": text,
        "category": category,
        "date": date,
        "embedding": embedding
    }

    collection.insert_one(doc)

    return jsonify({"message": "Document ingested successfully!"})
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "query is required"}), 400

    results = hybrid_search(query)
    return jsonify({"query": query, "results": results})
@app.route('/debug-embedding', methods=['GET'])
def debug_embedding():
    result = get_embedding("test sentence")
    return jsonify({
        "type": str(type(result)),
        "length": len(result) if isinstance(result, list) else "not a list",
        "sample": result[:3] if isinstance(result, list) else result
    })
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
