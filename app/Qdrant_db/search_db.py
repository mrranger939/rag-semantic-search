from app.Qdrant_db.initialise_db import client, COLLECTION


def search(vector, limit):
    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=limit
    )

    return results.points
