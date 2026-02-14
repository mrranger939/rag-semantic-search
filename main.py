from app.data import documents
from app.embedder import embed
from app.vector_store import create_collection, insert
from app.search import search_query

create_collection()

vectors = embed(documents)
insert(vectors, documents)

query = input("Ask something: ")
results = search_query(query)

print("\nResults:")
for r in results:
    print("-", r)
