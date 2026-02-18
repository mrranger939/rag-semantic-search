from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv
import os
load_dotenv()
client = QdrantClient("localhost", port=6333)

COLLECTION = os.getenv("QDRANT_COLLECTION")

def init_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            ),
        )

def insert(vectors, texts):
    client.upload_collection(
        collection_name=COLLECTION,
        vectors=vectors,
        payload=[{"text": t} for t in texts],
    )

def search(vector, limit):
    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=limit
    )

    return results.points
