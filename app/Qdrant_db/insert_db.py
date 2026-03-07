from qdrant_client.models import PointStruct
from app.Qdrant_db.initialise_db import client, COLLECTION
from app.generate_hash import generate_doc_id


def build_points(vectors, texts, metadata_list):
    
    points = []

    for vector, text, metadata in zip(vectors, texts, metadata_list):
        doc_id = generate_doc_id(text)
        payload = {
            "text": text,
            **metadata
        }

        points.append(
            PointStruct(
                id=doc_id,
                vector=vector,
                payload=payload
            )
        )

    return points


def insert(vectors, texts, metadata_list):
    points = build_points(vectors, texts, metadata_list)

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )
