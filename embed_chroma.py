import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from tqdm import tqdm

# Load CSV
df = pd.read_csv("data/arxiv_cleaned.csv")

# Load embedding model
print("📦 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Init persistent ChromaDB client
print("🔧 Initializing persistent ChromaDB client...")
client = PersistentClient(path="./chroma")
collection = client.get_or_create_collection(name="arxiv-papers")

# Clear existing entries (optional)
# collection.delete(where={})

# Embed and add documents
print("🧠 Embedding texts and uploading to ChromaDB...")
for i, row in tqdm(df.iterrows(), total=len(df)):
    doc_id = str(row["id"])
    text = f"{row['title']} {row['abstract']}"
    embedding = model.encode(text).tolist()
    metadata = {
        "title": row["title"],
        "url": f"https://arxiv.org/abs/{row['id']}",
        "categories": row["categories"],
        "date": row.get("update_date", "N/A")
    }
    collection.add(documents=[text], ids=[doc_id], embeddings=[embedding], metadatas=[metadata])

print("✅ Done. Your data is now persisted in ./chroma/")
