from kafka import KafkaProducer;
import json
import time
import random
import os
from dotenv import load_dotenv
load_dotenv()
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = os.getenv("KAFKA_TOPIC")

documents = [
    "Refund delayed due to payment gateway issue",
    "User unable to login after password reset",
    "Shipping delayed because of weather conditions",
    "Order cancellation requested by customer",
    "Payment processed successfully"
]

while True:
    message = {
        "text": random.choice(documents)
    }

    producer.send(TOPIC, message)
    print("Sent:", message)

    time.sleep(2)