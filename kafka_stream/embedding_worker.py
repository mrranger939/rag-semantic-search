from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
from app.embedder import embed
from app.vector_store import insert, init_collection
import os

load_dotenv()

init_collection()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="qdrant-ingestion-group"

)

print("Embedding worker started...")

while True:
    message_batch = consumer.poll(timeout_ms=10000)
    if not message_batch:
        continue
    for topic_partition, messages in message_batch.items():
        texts_to_embed = []
        for message in messages:
            texts_to_embed.append(message.value['text'])
        try:
            vectors = embed(texts_to_embed)
            insert(vectors, texts_to_embed)
            consumer.commit()
            print(f"Successfully processed and committed batch of {len(texts_to_embed)} documents.")

        except Exception as e:
            print(f"Failed to process batch: {e}. Offset not committed. Will retry.")


