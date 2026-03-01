from kafka import KafkaProducer;
import json
import time
import os
from dotenv import load_dotenv
import nltk
from nltk.tokenize import sent_tokenize

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = os.getenv("KAFKA_TOPIC")

nltk.download('punkt_tab')
with open("data/alice_in_wonderland.txt", "r", encoding="utf-8") as f:
    text = f.read()


sentences = sent_tokenize(text)
CHUNK_SIZE = 5
chunks = []

for i in range(0, len(sentences), CHUNK_SIZE):
    chunk_text = " ".join(sentences[i:i + CHUNK_SIZE])
    chunks.append(chunk_text)


BATCH_SIZE = 3   
index = 0

while True:
    batch = chunks[index:index + BATCH_SIZE]

    if not batch:
        index = 0
        continue

    for chunk in batch:
        message = {"text": chunk}
        producer.send(TOPIC, message)
        print("Sent chunk:\n", chunk[:100], "...")  

    index += BATCH_SIZE
    time.sleep(2)