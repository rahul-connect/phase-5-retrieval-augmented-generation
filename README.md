# Phase 5 — Retrieval-Augmented Generation (RAG)

Hands-on development of Retrieval-Augmented Generation (RAG) systems using **Python, Google Gemini Embeddings, PostgreSQL, pgvector, Groq, Jina AI, and FastAPI**.

This repository is part of my **AI Engineering Learning Roadmap**, documenting my progression from understanding text embeddings and vector similarity to building, improving, and evaluating RAG applications.

The emphasis is on understanding not just how to connect an LLM to a database, but why retrieval systems fail, how to improve their quality, and how to measure their performance.

**Current status:** Lessons 01–08 completed. The final capstone will be added separately after completion.

---

## What Is RAG?

Retrieval-Augmented Generation (RAG) is an approach that combines information retrieval with language model generation.

Instead of relying only on the knowledge stored in a model's parameters, a RAG application retrieves relevant information from an external knowledge base and supplies it as context when generating an answer.

A typical RAG workflow:

```text
Documents
   |
   v
Chunking
   |
   v
Embedding Model (Google Gemini)
   |
   v
PostgreSQL + pgvector
   |
   |  User Question
   |       |
   |       v
   |  Query Embedding
   |       |
   +-------+
           |
           v
    Vector Retrieval
           |
           v
    Retrieval Improvements
    (Filtering / Reranking)
           |
           v
    Relevant Context
           |
           v
       Groq LLM
           |
           v
    Grounded Response
```

This repository explores the components of that pipeline individually before combining them into a working backend application.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Google Gemini Embeddings | Text-to-vector representations |
| PostgreSQL | Relational database |
| pgvector | Vector storage and similarity search |
| SQLAlchemy | Python database integration |
| Groq API | LLM inference and answer generation |
| Jina AI | Retrieval reranking |
| FastAPI | REST API development |
| Server-Sent Events | Streaming generated responses |
| Pydantic | Data validation and application schemas |
| uv | Python dependency management |

---

## Curriculum

| Lesson | Topic | Main Concepts |
|---|---|---|
| 01 | [Embeddings](lesson-01-embeddings/) | Embedding generation, vectors, semantic similarity |
| 02 | [Chunking](lesson-02-chunking/) | Document splitting, chunk size, overlap |
| 03 | [Vector Databases](lesson-03-vector-db/) | PostgreSQL, pgvector, vector similarity search |
| 04 | [RAG Pipeline](lesson-04-rag-pipeline/) | Retrieval, context construction, LLM generation |
| 05 | [Better Retrieval](lesson-05-better-retrieval/) | Hybrid retrieval, filtering, reranking |
| 06 | [FastAPI RAG](lesson-06-fastapi-rag/) | Ingestion and query API development |
| 07 | [Streaming RAG](lesson-07-streaming-rag/) | Streaming generation, SSE |
| 08 | [RAG Evaluation](lesson-08-evaluation/) | Retrieval metrics, answer evaluation, evaluation workflows |

---

## Part I — Understanding the Components

### Lesson 01 — Embeddings

**Folder:** `lesson-01-embeddings/`

Introduction to semantic representations of text.

**Concepts explored:**

- What embeddings are and why they exist
- Converting text into numerical vectors
- Embedding dimensionality
- Semantic similarity
- Comparing vectors
- Similarity and distance metrics
- Using Google's embedding API

The goal is to understand how meaning can be represented numerically before introducing vector databases.

### Lesson 02 — Document Chunking

**Folder:** `lesson-02-chunking/`

Understanding how documents are divided into smaller retrievable units.

**Concepts explored:**

- Why documents need chunking
- Chunk size
- Chunk overlap
- Different splitting strategies
- Preserving context
- Chunk boundaries
- Trade-offs between retrieval precision and context completeness

Chunking directly affects what information a retrieval system can find.

### Lesson 03 — Vector Databases

**Folder:** `lesson-03-vector-db/`

Storing and retrieving embeddings using PostgreSQL and pgvector.

**Concepts explored:**

- Vector databases
- PostgreSQL's pgvector extension
- Vector columns
- Embedding storage
- Similarity and distance calculations
- Top-K retrieval
- SQL vector queries
- Integrating vector operations with Python

This lesson connects the RAG curriculum to the PostgreSQL concepts introduced in Phase 3.

---

## Part II — Building and Improving RAG

### Lesson 04 — First RAG Pipeline

**Folder:** `lesson-04-rag-pipeline/`

Combining embeddings, chunking, vector storage, retrieval, and LLM inference into an end-to-end RAG workflow.

**Concepts explored:**

- Document ingestion
- Text chunking
- Embedding generation
- Storing document chunks
- Query embedding
- Retrieving relevant context
- Top-K similarity search
- Constructing grounded prompts
- Generating answers with Groq

The objective is to understand how the individual RAG components work together.

### Lesson 05 — Better Retrieval

**Folder:** `lesson-05-better-retrieval/`

Exploring limitations of basic vector similarity search and techniques for improving retrieval quality.

**Concepts explored:**

- Irrelevant retrieved chunks
- Missing relevant information
- Similarity thresholds
- Metadata filtering
- Hybrid retrieval concepts
- Semantic versus keyword search
- Reranking
- Jina AI reranking
- Candidate retrieval and reranking trade-offs
- Precision and recall considerations

This lesson emphasizes the distinction between retrieving documents that appear similar and retrieving information that is genuinely useful for answering a question.

---

## Part III — RAG Backend Engineering

Lessons 06–08 develop a small FastAPI-based RAG application incrementally.

### Lesson 06 — FastAPI RAG

**Folder:** `lesson-06-fastapi-rag/`

Exposing RAG functionality through a backend API.

**Concepts explored:**

- FastAPI application structure
- Document ingestion workflows
- Query endpoints
- Pydantic request and response models
- Dependency injection
- Database integration
- Separating retrieval and generation logic
- API error handling

This lesson connects RAG development to the backend architecture introduced in Phase 2.

### Lesson 07 — Streaming RAG

**Folder:** `lesson-07-streaming-rag/`

Extending the RAG API to deliver generated responses incrementally.

**Concepts explored:**

- Streaming LLM responses
- Python generators
- Incremental output
- Server-Sent Events (SSE)
- Streaming HTTP responses
- Retrieval before generation
- Handling streaming failures
- Understanding response latency

This builds on the streaming concepts introduced in Phase 4.

### Lesson 08 — RAG Evaluation

**Folder:** `lesson-08-evaluation/`

Understanding how to evaluate retrieval and generated answers systematically.

**Concepts explored:**

- Why RAG evaluation matters
- Evaluation datasets
- Question and expected-answer pairs
- Retrieval relevance
- Precision and recall
- Recall@K
- Answer quality
- Groundedness and faithfulness concepts
- Automated evaluation workflows
- LLM-as-a-judge
- Comparing retrieval configurations

Evaluation helps identify failures that may not be obvious from testing a few example questions manually.

---

## Project Development Approach

This phase follows an incremental development structure.

**Lessons 01–03:** Standalone Python scripts exploring embeddings, chunking, and vector databases independently.

**Lessons 04–05:** Standalone RAG scripts, with Lesson 05 extending and improving the retrieval pipeline introduced in Lesson 04.

**Lessons 06–08:** A small FastAPI RAG application developed across successive lessons, adding API functionality, streaming, and evaluation.

Each lesson directory preserves the work associated with that learning stage.

---

## Getting Started

### Prerequisites

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL
- pgvector extension
- Google Gemini API key
- Groq API key
- Jina API key for lessons using reranking

### 1. Clone the Repository

```bash
git clone https://github.com/rahul-connect/phase-5-retrieval-augmented-generation.git
cd phase-5-retrieval-augmented-generation
```

### 2. Install Dependencies

Navigate to the lesson you want to explore:

```bash
cd lesson-04-rag-pipeline
uv sync
```

Each lesson may define its own dependencies in `pyproject.toml`.

### 3. Configure Environment Variables

Copy the example environment file if one is provided:

```bash
cp .env.example .env
```

Update the required credentials and database connection settings.

The environment variables differ by lesson:

| Lessons | Required Configuration |
|---|---|
| 01–02 | `GOOGLE_API_KEY` |
| 03 | `GOOGLE_API_KEY`, `DATABASE_URL` |
| 04 | `GOOGLE_API_KEY`, `DATABASE_URL`, `GROQ_API_KEY`, `GROQ_MODEL_NAME` |
| 05–08 | Google, PostgreSQL, Groq, and Jina configuration |

Example for later lessons:

```env
GOOGLE_API_KEY=your-google-gemini-api-key-here
DATABASE_URL=postgresql+psycopg://USER@localhost:5432/sql_learning
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL_NAME=openai/gpt-oss-120b
JINA_API_KEY=your-jina-api-key-here
JINA_URL=your-configured-jina-reranking-endpoint
JINA_MODEL=your-configured-jina-reranker-model
```

The actual database connection and model configuration depend on your local environment and available provider models.

Never commit real API keys or database credentials.

### 4. Configure PostgreSQL and pgvector

Ensure PostgreSQL is running and create a development database if needed:

```sql
CREATE DATABASE sql_learning;
```

Connect to the development database and enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The pgvector extension must already be installed on the PostgreSQL server.

The database schema and seed data required by individual lessons should be initialized using the corresponding lesson's SQL scripts or migrations.

### 5. Run a Lesson

For standalone Python lessons, run the relevant script using `uv run`.

For FastAPI lessons, use the actual application entry point defined in the lesson project.

If the FastAPI application is named `app` in `main.py`:

```bash
uv run uvicorn main:app --reload
```

The interactive API documentation is normally available at:

http://127.0.0.1:8000/docs

---

## Engineering Concepts

### Retrieval Engineering

- Embeddings and semantic similarity
- Document chunking
- Vector databases
- Top-K retrieval
- Metadata filtering
- Hybrid retrieval
- Reranking
- Retrieval precision and recall

### LLM Application Development

- Context-grounded generation
- Prompt construction
- LLM inference
- Streaming generation
- Handling retrieved context
- Understanding hallucination risks

### Backend and Database Engineering

- FastAPI
- PostgreSQL
- pgvector
- SQLAlchemy
- Pydantic
- Database queries
- API development
- Dependency management

### Evaluation and Reliability

- Retrieval evaluation
- Answer quality measurement
- Evaluation datasets
- Recall@K
- LLM-as-a-judge concepts
- Latency and token usage trade-offs
- Understanding retrieval failure modes

---

## Repository Structure

```text
phase-5-retrieval-augmented-generation/
│
├── lesson-01-embeddings/
├── lesson-02-chunking/
├── lesson-03-vector-db/
├── lesson-04-rag-pipeline/
├── lesson-05-better-retrieval/
├── lesson-06-fastapi-rag/
├── lesson-07-streaming-rag/
├── lesson-08-evaluation/
│
├── .gitignore
└── README.md
```

---

## Learning Progression

This repository represents **Phase 5 of my AI Engineering Learning Roadmap**.

**Phase 0 — Python Foundations:** Core Python programming.

**Phase 1 — Modern Python Development:** Python tooling, typing, testing, asynchronous programming, and application structure.

**Phase 2 — FastAPI Backend Development:** REST APIs, dependency injection, middleware, and backend architecture.

**Phase 3 — PostgreSQL & Database Engineering:** SQL, relational modeling, SQLAlchemy, Alembic, and database-backed applications.

**Phase 4 — LLM Application Development:** LLM APIs, prompt engineering, conversations, structured outputs, streaming, and tool use.

**Phase 5 — Retrieval-Augmented Generation:** Embeddings, chunking, vector retrieval, RAG pipelines, retrieval improvements, streaming APIs, and evaluation.

---

## Current Status

**Lessons 01–08 completed.**

The repository currently contains the completed lesson exercises and incremental RAG application work.

The final capstone will be added in a future update after implementation.

This is a learning and portfolio repository, not a production-ready RAG service.