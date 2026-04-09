from app.embedder import embed
from app.Qdrant_db.search_db import dense_search, sparse_search


def rrf_fusion(dense_results, sparse_results, k=60):
    scores = {}

    for rank, hit in enumerate(dense_results):
        doc_id = hit.id
        scores.setdefault(doc_id, 0)
        scores[doc_id] += 1/(k + rank + 1)

    for rank, hit in enumerate(sparse_results):
        doc_id = hit.id
        scores.setdefault(doc_id, 0)
        scores[doc_id] += 1 / (k + rank + 1)

    id_to_hit = {}
    for hit in dense_results + sparse_results:
        id_to_hit[hit.id] = hit

    reranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [id_to_hit[doc_id] for doc_id, _ in reranked]
    



def search_query(query, limit):
    print(f"Searching for: '{query}'...")
    dense_vectors, sparse_vectors = embed([query])
    dense_vector = dense_vectors[0]
    sparse_vector = sparse_vectors[0]
    dense_results = dense_search(dense_vector, limit=10)
    sparse_results = sparse_search(
        {
            "indices": sparse_vector.indices.tolist(),
            "values": sparse_vector.values.tolist()
        },
        limit=10
    )
    fused_results = rrf_fusion(dense_results, sparse_results)

    final_hits = fused_results[:limit]

    context_blocks = []

    for hit in final_hits:
        doc_text = hit.payload.get('text', '')
        source = hit.payload.get("source", "unknown")

        context_blocks.append(
            f"Document: {source}\nContent:\n{doc_text}"
        )

    return "\n---\n".join(context_blocks)


