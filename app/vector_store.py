from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient("localhost", port=6333)

COLLECTION = "documents"

def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

def insert(vectors, texts):
    client.upload_collection(
        collection_name=COLLECTION,
        vectors=vectors,
        payload=[{"text": t} for t in texts],
    )

def search(vector):
    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=3
    )

    return results.points
