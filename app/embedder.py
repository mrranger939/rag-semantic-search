from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(texts):
    return model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32
    )
