from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load persistent ChromaDB
client = PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="arxiv-papers")

class Query(BaseModel):
    question: str
    top_k: int = 5

@app.post("/search")
def search_articles(query: Query):
    embedding = model.encode(query.question).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=query.top_k)
    output = []
    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        output.append({
            "title": metadata.get("title"),
            "url": metadata.get("url"),
            "categories": metadata.get("categories"),
            "date": metadata.get("date"),
            "excerpt": results["documents"][0][i][:300] + "..."
        })
    return {"results": output}
