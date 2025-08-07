# search_api.py

from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import Client
from sentence_transformers import SentenceTransformer

# Initialize FastAPI
app = FastAPI(title="TrustAI — arXiv Article Recommender")

# Load model + Chroma
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Client()
collection = client.get_or_create_collection("arxiv-papers")

# Request schema
class Query(BaseModel):
    question: str
    top_k: int = 5

@app.post("/search")
def search_articles(query: Query):
    query_embedding = model.encode(query.question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=query.top_k
    )

    # Format output
    response = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        response.append({
            "title": meta["title"],
            "url": meta["url"],
            "categories": meta["categories"],
            "date": meta["date"],
            "excerpt": doc[:300] + "..." if doc else ""
        })

    return {"results": response}