---
title: Dynamic RAG API
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---





# RAG System (v1.0)

A **production-oriented Retrieval-Augmented Generation (RAG) system** that answers questions **strictly grounded in provided documents**, with dynamic hallucination control and FastAPI deployment.

This project focuses on **correct RAG behavior** (grounded answers + refusal for out-of-scope queries), not chatbot-style guessing.

---

## 🚀 Features

- 📄 Document ingestion from local files (TXT / PDF / Web-ready)
- 🔍 Vector search using **FAISS**
- 🧠 **Cross-encoder reranking** for improved retrieval quality
- 🚫 **Dynamic refusal** of out-of-scope questions (hallucination control)
- 📊 Evaluation with **relevance** and **faithfulness** metrics
- ⚡ **FastAPI backend** for serving RAG as an API
- 🔁 **Dataset-agnostic** (no hardcoded domain logic)

---

## 🧱 High-Level Architecture

```
User Query
   ↓
Retriever (FAISS)
   ↓
Reranker (Cross-Encoder)
   ↓
Semantic Relevance Gate
   ↓
LLM (Answer Generation)
```

If the retrieved context is insufficient or irrelevant, the system **refuses to answer** instead of hallucinating.

---

## 📡 API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{ "status": "ok" }
```

---

### Query RAG
```
POST /query
```

**Request**
```json
{
  "question": "Name some companies mentioned in the document"
}
```

**Response (in-scope query)**
```json
{
  "answer": "Samsung, TCS, Infosys, Reliance, Apple, Tesla, IBM, Intel, Amazon, Meta, NVIDIA."
}
```

**Response (out-of-scope query)**
```json
{
  "answer": "Not found in document"
}
```

---

## 🗂 Project Structure

```
RAG-SYSTEM/
├── app/
│   ├── api.py            # FastAPI routes
│   ├── rag_chain.py      # Core RAG orchestration
│   ├── retriever.py      # Document loading + FAISS
│   ├── reranker.py       # Cross-encoder reranker
│   ├── llm.py            # LLM loading & inference
│   ├── evaluation/       # Relevance & faithfulness metrics
│   └── data/docs/        # Knowledge base (TXT / PDF files)
│
├── main.py               # API entrypoint
├── requirements.txt
└── README.md
```

---

## ▶️ Running Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API
```bash
python main.py
```

API will be available at:
```
http://127.0.0.1:8000
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## 📊 Evaluation Philosophy

- **Relevance**: Measures semantic alignment between question and retrieved context
- **Faithfulness**: Measures how much of the answer is supported by the context

Low faithfulness scores for abstract or summarized answers are expected and do **not** necessarily indicate hallucination.

The primary correctness signal is **dataset-grounded refusal** for unsupported queries.

---

## 🛠 Tech Stack

- Python
- LangChain
- FAISS
- Hugging Face Transformers
- Sentence-Transformers
- PyTorch
- FastAPI

---

## 📦 Versioning

- **v1.0** — Text-only RAG with FastAPI deployment
- **v1.1 (planned)** — Persistent FAISS index (save/load)
- **v1.2 (planned)** — Dockerized deployment
- **v2.0 (planned)** — Multimodal RAG (text + images)

---

## 📜 License

MIT License

---

## 🧠 Notes

This project intentionally prioritizes **correct RAG behavior** over conversational fluency:
- The system answers **only when evidence exists**
- Otherwise, it explicitly refuses

This design mirrors real-world, production RAG systems used for enterprise and knowledge-grounded applications.

