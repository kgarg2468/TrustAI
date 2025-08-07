import json
import os
from datetime import datetime

LOG_DIR = "logs"
QUERY_LOG = os.path.join(LOG_DIR, "query_log.jsonl")
VIEW_LOG = os.path.join(LOG_DIR, "view_log.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def log_query(query: str):
    with open(QUERY_LOG, "a") as f:
        entry = {"query": query, "timestamp": datetime.utcnow().isoformat()}
        f.write(json.dumps(entry) + "\n")

def log_view(paper_id: str, title: str):
    with open(VIEW_LOG, "a") as f:
        entry = {"paper_id": paper_id, "title": title, "timestamp": datetime.utcnow().isoformat()}
        f.write(json.dumps(entry) + "\n")