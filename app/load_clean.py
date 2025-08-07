# step1_load_clean_jsonl.py

import json
import pandas as pd
import os

# Input/output paths
input_path = "data/arxiv-metadata-oai-snapshot.json"
output_path = "data/arxiv_cleaned.csv"

# Confirm file exists
assert os.path.exists(input_path), f"Missing file: {input_path}"

# Load and parse JSONL
print("Loading JSON lines...")
data = []
with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            item = json.loads(line)
            data.append({
                "id": item.get("id"),
                "title": item.get("title", "").strip().replace("\n", " "),
                "abstract": item.get("abstract", "").strip().replace("\n", " "),
                "categories": item.get("categories", ""),
                "update_date": item.get("update_date", "")
            })
        except json.JSONDecodeError:
            continue

# Convert to DataFrame
df = pd.DataFrame(data)
df.dropna(inplace=True)

# Filter: remove too-short abstracts
df = df[df['abstract'].str.len() > 100]

# Limit for now to keep things fast
df = df.head(50000).reset_index(drop=True)

# Save
df.to_csv(output_path, index=False)
print(f"Saved cleaned data to: {output_path}")
print(df.sample(3))