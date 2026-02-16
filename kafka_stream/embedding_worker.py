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
    enable_auto_commit=True,
)

print("Embedding worker started...")

for message in consumer:
    text = message.value['text']
    vector = embed([text])
    insert(vector, [text])
    print("Stored: ", text)
