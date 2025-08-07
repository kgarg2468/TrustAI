from fastapi import APIRouter
import json
from collections import Counter

router = APIRouter()

def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- Endpoint 1: Get most common queries
@router.get("/analytics/queries")
def get_top_queries(limit: int = 10):
    queries = load_json("logs/query_log.json")
    counter = Counter(queries)
    return counter.most_common(limit)

# --- Endpoint 2: Get most viewed papers
@router.get("/analytics/views")
def get_top_views(limit: int = 10):
    views = load_json("logs/view_log.json")
    counter = Counter(views)
    return counter.most_common(limit)