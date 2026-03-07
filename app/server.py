from fastapi import FastAPI
from kafka import KafkaProducer;
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from app.services.ingestion import ingest_text
from app.services.chat_service import chat

load_dotenv()

app = FastAPI()

# nltk.download('punkt')

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
print("Kafka connected successfully")
TOPIC = os.getenv("KAFKA_TOPIC")



@app.get('/')
def root():
    return {"message": "Hello"}


class IngestRequest(BaseModel):
    text: str

@app.post("/ingest/text")
def ingest(req:IngestRequest):
    return ingest_text(text=req.text, producer=producer, topic=TOPIC)


class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.question)
