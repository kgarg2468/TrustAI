import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load ChromaDB collection
chroma_client = chromadb.PersistentClient(path="chroma")
collection = chroma_client.get_or_create_collection("arxiv-papers")

# Custom search with cosine similarity and sentence highlighting
def search(query, top_k=20):
    query_embedding = embedding_model.encode(query, normalize_embeddings=True)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["metadatas", "documents", "embeddings"]
    )

    scored_results = []

    for i in range(len(results["documents"][0])):
        abstract = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        doc_embedding = np.array(results["embeddings"][0][i])
        doc_embedding = doc_embedding / np.linalg.norm(doc_embedding)

        similarity = float(np.dot(query_embedding, doc_embedding))

        print(f"[{i}] Title: {metadata.get('title')} | Similarity: {round(similarity, 3)}")

        if similarity < 0.4:
            continue

        sentences = abstract.split(". ")
        sent_embeddings = embedding_model.encode(sentences, normalize_embeddings=True)
        sent_scores = util.cos_sim(query_embedding, sent_embeddings)[0]
        top_indices = np.argsort(-sent_scores)[:2]
        highlights = [sentences[j].strip() for j in top_indices]

        scored_results.append({
            "title": metadata.get("title", "Unknown"),
            "url": metadata.get("url", ""),
            "similarity": round(similarity, 3),
            "highlights": highlights
        })

    return {"query": query, "results": scored_results}


# Test
if __name__ == "__main__":
    from pprint import pprint
    pprint(search("obesity"))