# embed_chroma.py

import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import Client
from tqdm import tqdm
import os

# Load cleaned dataset
df = pd.read_csv("data/arxiv_cleaned.csv")
texts = (df['title'] + ". " + df['abstract']).tolist()

# Load model and embed
print("📦 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("🧠 Embedding texts...")
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

# ✅ NEW CLIENT SYNTAX (no Settings)
client = Client()

# Optional: delete existing collection if needed
# client.delete_collection("arxiv-papers")

collection = client.get_or_create_collection("arxiv-papers")

# Add documents
print("📤 Adding documents to ChromaDB...")
for i in tqdm(range(len(df))):
    collection.add(
        documents=[texts[i]],
        embeddings=[embeddings[i]],
        metadatas=[{
            "title": df.loc[i, "title"],
            "categories": df.loc[i, "categories"],
            "date": df.loc[i, "update_date"],
            "url": f"https://arxiv.org/abs/{df.loc[i, 'id']}"
        }],
        ids=[str(i)]
    )

print("✅ Done. Your data is now in ChromaDB (in-memory).")