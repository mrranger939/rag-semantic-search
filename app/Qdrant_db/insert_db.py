from qdrant_client.models import PointStruct
from app.Qdrant_db.initialise_db import client, COLLECTION
from app.generate_hash import generate_doc_id


def build_points(dense_vectors, sparse_vectors, texts, metadata_list):
    
    points = []

    for dense, sparse, text, metadata in zip(dense_vectors, sparse_vectors, texts, metadata_list):
        doc_id = generate_doc_id(text)
        payload = {
            "text": text,
            **metadata
        }

        points.append(
            PointStruct(
                id=doc_id,
                vector={
                    "dense": dense,
                    "sparse": {
                        "indices": sparse.indices.tolist(),
                        "values": sparse.values.tolist()
                    }
                },
                payload=payload
            )
        )

    return points


def insert(dense_vectors, sparse_vectors, texts, metadata_list):
    points = build_points(dense_vectors, sparse_vectors, texts, metadata_list)

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )
