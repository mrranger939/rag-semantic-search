from kafka import KafkaConsumer
import json
import time
from dotenv import load_dotenv
from app.embedder import embed
from app.Qdrant_db.insert_db import insert
from app.Qdrant_db.initialise_db import init_collection
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

BATCH_INTERVAL = int(os.getenv("KAFKA_CONSUMER_BATCH_INTERVAL", 10))
MAX_BATCH_SIZE = int(os.getenv("KAFKA_CONSUMER_MAX_BATCH_SIZE", 50))
buffer = []
last_flush_time = time.time()

while True:
    records = consumer.poll(timeout_ms=1000)
    for _, messages in records.items():
        for message in messages:
            buffer.append(message.value['text'])

    now = time.time()

    
    if buffer and (len(buffer)>=MAX_BATCH_SIZE or (now - last_flush_time >= BATCH_INTERVAL)):
        try:
            vectors = embed(buffer)
            insert(vectors, buffer)
            consumer.commit()
            print(f"Successfully processed and committed batch of {len(buffer)} documents.")
            buffer.clear()
            last_flush_time = now

        except Exception as e:
            print(f"Failed to process batch: {e}.")
            raise e



