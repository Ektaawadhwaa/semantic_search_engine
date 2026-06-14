from flask import Flask, request, jsonify
from flask_cors import CORS
from search import hybrid_search, collection
from embeddings import get_embedding

app = Flask(__name__)
CORS(app)


@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        data = request.get_json(silent=True) or {}

        text = data.get('text', '').strip()
        category = data.get('category', 'general')
        date = data.get('date', '2025-01-01')

        if not text:
            return jsonify({"error": "text is required"}), 400

        # Generate embedding
        embedding = get_embedding(text)

        # Document to store
        doc = {
            "text": text,
            "category": category,
            "date": date,
            "embedding": embedding
        }

        collection.insert_one(doc)

        return jsonify({
            "message": "Document ingested successfully",
            "category": category
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json(silent=True) or {}

        query = data.get('query', '').strip()
        top_k = int(data.get('top_k', 3))

        if not query:
            return jsonify({"error": "query is required"}), 400

        results = hybrid_search(query, top_k)

        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "semantic-search-api"
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)