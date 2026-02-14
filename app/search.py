from app.embedder import embed
from app.vector_store import search

def search_query(query):
    vector = embed([query])[0]
    results = search(vector)

    return [r.payload["text"] for r in results]
