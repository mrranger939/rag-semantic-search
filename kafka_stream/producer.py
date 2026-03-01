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

BATCH_SIZE = 5
index = 0

while True:
    batch = sentences[index:index + BATCH_SIZE]

    if not batch:
        index = 0
        continue

    for sentence in batch:
        message = {"text": sentence}
        producer.send(TOPIC, message)
        print("Sent:", sentence)

    index += BATCH_SIZE
    time.sleep(2)