# Enterprise Agentic RAG Pipeline

An event-driven, microservice-based Retrieval-Augmented Generation (RAG) system designed for scalable document ingestion, hybrid retrieval accuracy, and self-correcting agentic reasoning.

This project demonstrates a **production-style AI architecture** with streaming ingestion, asynchronous embedding, hybrid search (dense + sparse), and autonomous query refinement.

---

# System Architecture

The system is composed of decoupled services connected through a streaming pipeline.

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
Kafka (Event Streaming Layer)
     │
     ▼
Embedding Worker (Async Processing)
     │
     ▼
Qdrant (Hybrid Vector Database)
     │
     ▼
LangGraph Agent (Reasoning Engine)
     │
     ▼
LLM (Answer Generation with Source Attribution)
```

---

# Project Structure

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
├── kafka_stream
│   ├── embedding_worker.py
│   └── producer.py
├── ui
│   └── frontend
│       └── app.py
├── main.py
├── questions.txt
├── README.md
├── requirements.txt
├── start.txt
```

---

# Core Capabilities

## 1. Asynchronous Ingestion Pipeline

* Documents (text or PDF) are accepted via API.
* Text is chunked using **sliding window strategy** (overlap preserved for context continuity).
* Chunks are streamed into Kafka.
* Prevents blocking API calls during large ingestion.

---

## 2. Decoupled Embedding Layer

* A standalone Kafka consumer processes document chunks.
* Generates:

  * Dense embeddings (semantic meaning)
  * Sparse embeddings (keyword signals)
* Stores both in Qdrant.

---

## 3. Hybrid Retrieval (Dense + Sparse)

* Dense vectors capture semantic similarity.
* Sparse vectors capture exact keyword matches.
* Retrieval performs:

  * Semantic search
  * Keyword search
* Results are merged using **Reciprocal Rank Fusion (RRF)**:

```
Score = 1 / (k + rank_dense) + 1 / (k + rank_sparse)
```

* Ensures both conceptual and exact matches are retrieved effectively.

---

## 4. Metadata Lineage

* Every document chunk retains metadata:

  * source (filename or user-defined)
* Enables deterministic answer attribution.
* LLM responses include source citations.

---

## 5. Agentic Reasoning (LangGraph)

The system uses a **state machine-based agent** instead of a single LLM call.

### Execution Flow

```
Start → Retrieve → Grade → (Rewrite OR Generate)
```

---

## 6. Self-Correcting Retrieval (Agentic RAG)

Two additional nodes enable autonomy:

### Grader Node

* Evaluates retrieved context against the query.
* Outputs: YES / NO

### Query Rewriter Node

* If context is not relevant:

  * rewrites the query
  * re-triggers retrieval

### Final Graph

```
Start
  ↓
Retrieve
  ↓
Grade
  ├── YES → Generate → End
  └── NO  → Rewrite → Retrieve (loop)
```

* Retry limit prevents infinite loops.
* Enables automatic recovery from poor retrieval.

---

# Project Features

## Feature 1: Foundation (MVP)

* End-to-end pipeline built
* Kafka-based ingestion
* Sliding window chunking
* FastAPI backend
* Streamlit UI
* LangGraph-based retrieval + generation
* Deterministic document identity via hashing

---

## Feature 2: Accuracy Upgrade (Hybrid Search)

* Dual vector storage (dense + sparse)
* BM25-style sparse embeddings
* Hybrid retrieval implementation
* Reciprocal Rank Fusion (RRF) integration
* Improved retrieval for:

  * exact keywords
  * codes
  * structured queries

---

## Feature 3: Autonomy Upgrade (Agentic RAG)

* Added grading node to evaluate retrieval quality
* Added query rewriting node
* Introduced cyclic graph execution
* Enabled retry-based retrieval correction
* Reduced "no information" failures

---

# Local Deployment

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Start Core Services

### Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

### Kafka

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

---

## 3. Run Application Services

### Terminal 1: Embedding Worker

```bash
python -m kafka_stream.embedding_worker
```

---

### Terminal 2: API Server

```bash
uvicorn app.server:app --reload --port 8000
```

---

### Terminal 3: UI

```bash
streamlit run .\ui\frontend\app.py
```

---

# Usage Flow

1. Upload a document (PDF or text)
2. System chunks and streams data to Kafka
3. Worker processes and indexes embeddings into Qdrant
4. User submits query
5. Agent:

   * retrieves relevant context
   * validates relevance
   * optionally rewrites query
   * generates final answer
6. Response includes cited document sources


