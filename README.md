
# RAG Semantic Search (Foundation)

A minimal semantic search system built using **sentence embeddings** and a **vector database**.
This project demonstrates the core retrieval layer used in Retrieval-Augmented Generation (RAG) pipelines.

The goal of this project is to build a clean and modular foundation that can later evolve into a real-time agentic RAG system using Kafka and multi-agent orchestration.

---

## Overview

Traditional keyword search fails when queries use different wording but have similar meaning.
Semantic search solves this by converting text into vector embeddings and retrieving results based on meaning rather than exact words.

This project implements:

```
Text Documents
      ↓
Embedding Model (Sentence Transformers)
      ↓
Vector Storage (Qdrant)
      ↓
Semantic Search (Top-K Retrieval)
```

---

## Features

* Sentence embeddings using HuggingFace Sentence Transformers
* Vector storage using Qdrant
* Cosine similarity based retrieval
* Modular architecture for future scalability
* Clean separation between embedding, storage, and search logic

---

## Project Structure

```
rag-semantic-search/
│
├── app/
│   ├── data.py           # Sample documents
│   ├── embedder.py       # Embedding generation
│   ├── vector_store.py   # Qdrant interaction
│   └── search.py         # Search logic
│
├── main.py               # Entry point
├── requirements.txt
└── README.md
```

---

## Tech Stack

* Python
* Sentence Transformers (HuggingFace)
* Qdrant Vector Database
* Docker

---

## How It Works

1. Documents are converted into embeddings using a pre-trained embedding model.
2. Embeddings are stored in Qdrant along with metadata.
3. A user query is converted into an embedding.
4. The system retrieves the most semantically similar documents.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mrranger939/rag-semantic-search
cd rag-semantic-search
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Dashboard:

```
http://localhost:6333/dashboard
```

---

### 5. Run the project

```bash
python main.py
```

Enter a query when prompted to retrieve similar documents.

---

## Example

Query:

```
I forgot my password
```

Result:

```
How to reset password?
How to change account email?
```

---

## Future Improvements

This project is the first step toward a larger system:

* Kafka-based real-time document ingestion
* Embedding worker service
* LangGraph-based multi-agent orchestration
* Retrieval grading and query rewriting
* Production-ready RAG pipeline

---

## Learning Objective

The purpose of this project is to understand:

* Embeddings and semantic similarity
* Vector databases
* Retrieval systems used in modern AI applications
* Foundations of scalable RAG architectures

