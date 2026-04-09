from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sparseModel = SparseTextEmbedding(model_name="Qdrant/bm25")
def embed(texts):
    dense_vectors = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32
    )
    sparse_vectors = list(sparseModel.embed(texts))

    return dense_vectors, sparse_vectors
