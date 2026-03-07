from fastapi import FastAPI
from kafka import KafkaProducer;
import json
import os
import uuid
from dotenv import load_dotenv
from pydantic import BaseModel
from app.services.ingestion import ingest_text
from app.services.chat_service import chat
from fastapi import UploadFile, File
import pdfplumber

load_dotenv()

app = FastAPI()

# nltk.download('punkt')

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
print("Kafka connected successfully!!")
TOPIC = os.getenv("KAFKA_TOPIC")

def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

@app.get('/')
def root():
    return {"message": "Hello"}


class IngestRequest(BaseModel):
    text: str
    source: str | None = None

@app.post("/ingest/text")
def ingest(req: IngestRequest):

    metadata = { 
        "source": req.source if req.source!="manual_text" else f"text_doc_{uuid.uuid4().hex[:6]}" 
        }

    return ingest_text(
        text=req.text,
        producer=producer,
        topic=TOPIC,
        metadata=metadata
    )


class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.question)

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):

    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    text = clean_text(text)

    metadata = {
        "source": file.filename
    }

    return ingest_text(
        text,
        producer=producer,
        topic=TOPIC,
        metadata=metadata
    )