#  Semantic Search Engine for MongoDB Documents

A full-stack AI-powered search engine that finds documents based on **meaning and intent**, not just exact keyword matches. Built with the MERN stack and Python NLP.

 **Live Demo:** (https://semantic-search-engine-henna.vercel.app)

---

##  Features

- **Semantic Search** — Understands the meaning behind queries using AI embeddings
- **Keyword Search** — Traditional full-text search via MongoDB Atlas Search
- **Hybrid Ranking** — Combines both approaches with weighted scoring for best results
- **Document Upload** — Add your own documents and search them instantly
- **REST API** — Clean API architecture with Node.js and Python microservices

---

##  Architecture


```
React (Vercel)
      ↓
Node.js / Express API
      ↓
Python Flask AI Service
      ↓
MongoDB Atlas (Vector Search + Atlas Search)
```


### How Semantic Search Works

1. Documents are converted into 384-dimensional vectors (embeddings) using `sentence-transformers/all-MiniLM-L6-v2`
2. Embeddings are stored in MongoDB Atlas alongside documents
3. When a user searches, the query is also converted to an embedding
4. MongoDB's Vector Search finds the most similar documents using cosine similarity
5. Results are combined with keyword search and ranked using weighted scoring



##  Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite, Axios |
| Backend API | Node.js, Express.js |
| AI / NLP | Python, Flask, Sentence Transformers |
| Database | MongoDB Atlas |
| Vector Search | MongoDB Atlas Vector Search |
| Keyword Search | MongoDB Atlas Search (BM25) |
| Deployment | Vercel (frontend), Render (backend) |

---

##  Project Structure


semantic-search-engine/
├── client/                  # React frontend
│   └── src/
│       ├── components/
│       │   ├── SearchBar.jsx
│       │   ├── ResultCard.jsx
│       │   └── UploadForm.jsx
│       └── App.jsx
├── server/                  # Node.js backend
│   ├── routes/
│   │   ├── search.js
│   │   └── ingest.js
│   └── index.js
└── python/               # Python AI microservice
    ├── app.py               # Flask API
    ├── search.py            # Hybrid search logic
    ├── embeddings.py        # Embedding generation
    └── requirements.txt



## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB Atlas account (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/Ektaawadhwaa/semantic_search_engine.git
cd semantic_search_engine
```

### 2. Setup MongoDB Atlas
- Create a free cluster at  (https://mongodb.com/atlas)
- Create database `semantic_search_db` with collection `documents`
- Create a **Vector Search index** named `vector_index`:
```json
{
  "fields": [
    { "type": "vector", "path": "embedding", "numDimensions": 384, "similarity": "cosine" },
    { "type": "filter", "path": "category" },
    { "type": "filter", "path": "date" }
  ]
}
```
- Create an **Atlas Search index** named `keyword_index` with dynamic mappings

### 3. Setup Python AI Service
```bash
cd python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `python/.env`:
```
MONGO_URI=your_mongodb_connection_string
DB_NAME=semantic_search_db
COLLECTION_NAME=documents
PRODUCTION=false
```

Run:
```bash
python app.py
```

### 4. Setup Node.js Server
```bash
cd server
npm install
```

Create `server/.env`:
```
PORT=5000
PYTHON_API_URL=http://localhost:5001
```

Run:
```bash
node index.js
```

### 5. Setup React Frontend
```bash
cd client
npm install
npm run dev
```

---
  
 
## 💡 Key Concepts

**Embeddings** — Text converted into 384 numbers that represent its meaning. Similar sentences produce similar numbers.

**Cosine Similarity** — Mathematical measure of how close two embeddings are. Score of 1.0 = identical meaning, 0.0 = completely different.

**Hybrid Search** — Combines semantic search (meaning-based) and keyword search (exact match) for higher accuracy than either alone.

**MongoDB Atlas Vector Search** — Stores and searches embeddings natively inside MongoDB, eliminating the need for external vector databases.

---

##   Deployment

| Service | Platform | URL |
|---|---|---|
| React Frontend | Vercel | [Live](https://semantic-search-engine-henna.vercel.app) |
| Node.js API | Render | https://semantic-search-node.onrender.com |
| Python AI API | Render | https://semantic-search-engine-yhcr.onrender.com |
| Database | MongoDB Atlas | 

> **Note:** Free tier services on Render may take 30-60 seconds to wake up after inactivity.

---

##   Future Enhancements

- [ ] Chat-based conversational search
- [ ] Multi-language support
- [ ] Automatic database query generation
- [ ] Document chunking for large files
- [ ] Advanced analytics dashboard
- [ ] Domain-specific embedding models

---

## 👩‍💻 Author

**Ekta Wadhwa**
- GitHub: [@Ektaawadhwaa](https://github.com/Ektaawadhwaa)