from app.search import search_query



query = input("Ask something: ")
results = search_query(query, limit=3)

print("\nResults:")
print(results)
