from app.embedder import embed
from app.Qdrant_db.search_db import search

def search_query(query, limit):
    print(f"Searching for: '{query}'...")
    vector = embed([query])[0]
    results = search(vector, limit)
    context_blocks = []
    for hit in results:
        doc_text = hit.payload.get('text', '')
        score = hit.score # The cosine similarity score
        context_blocks.append(f"[Score: {score:.2f}] {doc_text}")
        
    final_context = "\n---\n".join(context_blocks)
    return final_context


