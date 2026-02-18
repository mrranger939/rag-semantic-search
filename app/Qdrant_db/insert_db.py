from qdrant_client.models import PointStruct
from app.Qdrant_db.initialise_db import client, COLLECTION
from app.generate_hash import generate_doc_id


def build_points(vectors, texts):
    
    points = []

    for vector, text in zip(vectors, texts):
        doc_id = generate_doc_id(text)
        points.append(
            PointStruct(
                id=doc_id,
                vector=vector,
                payload={"text": text}
            )
        )

    return points


def insert(vectors, texts):
    points = build_points(vectors, texts)

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )
