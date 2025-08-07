from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.search_api import search
from app.analytics_api import router as analytics_router

app = FastAPI(title="TrustAI: Article Recommender")

# Enable CORS for local testing or frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Search endpoint
@app.get("/search")
def search_endpoint(query: str = Query(..., description="Your search term")):
    return search(query)

# Mount analytics API routes
app.include_router(analytics_router)