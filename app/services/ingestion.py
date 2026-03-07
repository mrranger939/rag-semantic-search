import tiktoken
from nltk.tokenize import sent_tokenize

CHUNK_SIZE = 250
OVERLAP = 50

tokenizer = tiktoken.get_encoding("cl100k_base")


def token_count(text):
    return len(tokenizer.encode(text))


def chunk_text(text):
    sentences = sent_tokenize(text)

    chunks = []
    chunk = []
    tokens = 0

    for sentence in sentences:
        sentence_tokens = token_count(sentence)

        if tokens + sentence_tokens > CHUNK_SIZE:
            chunks.append(" ".join(chunk))

            # overlap
            overlap_chunk = []
            overlap_tokens = 0

            for s in reversed(chunk):
                t = token_count(s)
                overlap_tokens += t
                overlap_chunk.insert(0, s)

                if overlap_tokens >= OVERLAP:
                    break

            chunk = overlap_chunk
            tokens = overlap_tokens

        chunk.append(sentence)
        tokens += sentence_tokens

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

def ingest_text(text: str, producer, topic: str):

    chunks = chunk_text(text)

    for chunk in chunks:
        producer.send(topic, {"text": chunk})

    producer.flush()

    return {
        "status": "queued",
        "chunks": len(chunks)
    }