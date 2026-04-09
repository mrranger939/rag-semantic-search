from app.Qdrant_db.initialise_db import client, COLLECTION
from qdrant_client.models import SparseVector

def dense_search(vector, limit):
    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        using='dense',
        limit=limit
    )

    return results.points

def sparse_search(sparse_vector, limit=10):
    query = SparseVector(
        indices=sparse_vector["indices"],   
        values=sparse_vector["values"]     
    )

    results = client.query_points(
        collection_name=COLLECTION,
        query=query,
        using="sparse",  
        limit=limit
    )

    return results.points   
