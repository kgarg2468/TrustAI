# main.py

from fastapi import FastAPI, Query
from app.search_api import search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TrustAI: Article Recommender")

# Enable CORS for local testing or frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_endpoint(query: str = Query(..., description="Your search term")):
    return search(query)