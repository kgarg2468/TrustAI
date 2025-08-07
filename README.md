# TrustAI

TrustAI is a local, lightweight article recommendation system designed to help users discover relevant research from the arXiv dataset based on their interests.

## Purpose

The assistant provides personalized recommendations based on users' interests in research and articles, helping them navigate the vast amount of available information more efficiently. By streamlining the discovery process, it enables users to stay informed and focused on the content most relevant to their goals.

This project emphasizes:

- Speed and local control over your data
- Use of open-source tools
- Minimal dependencies
- Personalized and intelligent suggestions

## Tech Stack

- Python 3.9+
- ChromaDB (Vector DB)
- SentenceTransformers (all-MiniLM-L6-v2)
- pandas
- tqdm

## How It Works

1. **Data Cleaning**: The raw arXiv dataset is cleaned to remove missing or irrelevant records.
2. **Embedding**: Research paper abstracts are embedded using a sentence-transformer model.
3. **Vector Storage**: These embeddings are stored in a persistent ChromaDB collection.
4. **Query**: The user inputs a research interest, and TrustAI returns top-k semantically similar papers.

## Project Structure

- `clean_arxiv.py`: Cleans and processes the original dataset
- `embed_chroma.py`: Embeds text using `all-MiniLM-L6-v2` and stores in ChromaDB
- `query_chroma.py`: Accepts user queries and returns relevant results
- `data/`: Contains input and cleaned CSVs
- `chroma/`: Stores persistent vector database files

## Notes

- The project uses local ChromaDB with persistent storage enabled. No internet is required after initial embedding.
- The embedding model is compact, fast, and runs well on CPUs.

## Setup

1. Clone the repo and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the cleaning step:
    ```bash
    python clean_arxiv.py
    ```

3. Embed and store data:
    ```bash
    python embed_chroma.py
    ```

4. Start querying:
    ```bash
    python query_chroma.py
    ```
