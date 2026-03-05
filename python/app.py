from flask import Flask, request, jsonify
from flask_cors import CORS
from search import hybrid_search
app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "query is required"}), 400

    results = hybrid_search(query)
    return jsonify({"query": query, "results": results})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
