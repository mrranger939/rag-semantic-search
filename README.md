
# Enterprise Agentic RAG Pipeline

An asynchronous, event-driven Retrieval-Augmented Generation (RAG) microservice architecture. Built for high-throughput document ingestion, highly accurate semantic retrieval, and hallucination-free LLM reasoning with strict metadata lineage.

## System Architecture

The pipeline decouples ingestion, embedding, and inference into independent, scalable microservices connected by a distributed message broker.

```text
Streamlit UI
     │
     ▼
FastAPI (API Gateway)
     │
     ├── POST /ingest/text
     ├── POST /ingest/pdf
     └── POST /chat
     │
     ▼
Kafka (Event Stream & Buffer)
     │
     ▼
Embedding Worker (Async ETL)
     │
     ▼
Qdrant (Vector & Metadata Storage)
     │
     ▼
LangGraph Agent (Reasoning & Retrieval)
     │
     ▼
LLM (Answer Generation & Source Citation)

```
## Project Structure

```
.
├── app
│   ├── agent
│   │   ├── graph.py
│   │   ├── llm.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── data.py
│   ├── embedder.py
│   ├── generate_hash.py
│   ├── Qdrant_db
│   │   ├── initialise_db.py
│   │   ├── insert_db.py
│   │   └── search_db.py
│   ├── search.py
│   ├── server.py
│   ├── services
│   │   ├── chat_service.py
│   │   └── ingestion.py
│   └── ui.py
├── data
│   ├── alice_in_wonderland.txt
│   ├── ML-1-10.pdf
│   └── ML-11-20.pdf
├── kafka_stream
│   ├── embedding_worker.py
│   └── producer.py
├── main.py
├── questions.txt
├── README.md
├── requirements.txt
└── start.txt
```

## Core Infrastructure

* **Asynchronous Ingestion (FastAPI + Kafka):** Documents are chunked using `tiktoken` (enforcing strict token limits and overlaps) and streamed into Kafka, preventing API timeouts during massive document uploads.
* **Decoupled Embedding (Python Worker):** A standalone worker continuously consumes the Kafka stream, generates vector embeddings, and upserts them into Qdrant.
* **Metadata Lineage:** Every chunk mathematically retains its origin data (e.g., `filename`, `source`). The LLM does not just answer; it cites the exact document it extracted the answer from.
* **State Machine Reasoning (LangGraph):** Inference is not a simple API call. It is a deterministic state graph that retrieves context, formats the prompt, and enforces strict boundary conditions on the LLM to prevent hallucinations.

## Local Deployment

### 1. Prerequisites

```bash
pip install -r requirements.txt

```

### 2. Boot Core Services (Docker)

**Start Qdrant (Vector DB):**

```bash
docker run -p 6333:6333 qdrant/qdrant

```

**Start Kafka (Message Broker):**

```bash
docker run -p 9092:9092 \
-e KAFKA_PROCESS_ROLES=broker,controller \
-e KAFKA_NODE_ID=1 \
-e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
-e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
-e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
-e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
confluentinc/cp-kafka

```

### 3. Initialize the Pipeline

You must run these three services simultaneously in separate terminals.

**Terminal 1: Start the Embedding Worker**

```bash
python -m kafka_stream.embedding_worker

```

**Terminal 2: Start the API Gateway**

```bash
uvicorn app.server:app --reload --port 8000

```

**Terminal 3: Start the UI**

```bash
streamlit run app/ui.py

```

## Workflow & Usage

1. **Ingest:** Upload a `.pdf` or paste raw text via the Streamlit UI. The API will parse, chunk, and stream the payload to Kafka.
2. **Process:** The Embedding Worker automatically consumes the stream and indexes the vectors into Qdrant.
3. **Query:** Ask a question in the chat interface. The LangGraph agent will execute a semantic search, inject the top chunks into the LLM context window, and return a deterministic answer citing the source document.
