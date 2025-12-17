# Dynamic Retrieval-Augmented Generation API

A **versioned, production-grade Retrieval-Augmented Generation (RAG) system**
that evolves from **text-only RAG** to a **Hybrid RAG (Text + Image OCR)** architecture.

---

## 📌 Versions Overview

| Version | Description |
|------|-------------|
| **v1** | Basic text-only RAG |
| **v1.1** | Improved chunking & retrieval |
| **v1.2** | Performance & API refinements |
| **v2.0.0** | 🚀 Hybrid RAG (Text + Image OCR, Query Expansion) |

---

## 🚀 What’s New in v2.0.0

- Hybrid RAG (Text + Image)
- OCR-based image ingestion (EasyOCR, GPU supported)
- Unified vector database (text + image knowledge)
- Query expansion for better recall
- Context-aware prompting
- Strict grounding (no hallucinations)
- FastAPI backend

---

## 🧠 Architecture

Text Files ─┐
            ├── Chunking → Embeddings → Vector DB
Images ─OCR─┘

User Query
   ↓
Query Expansion
   ↓
Retriever
   ↓
Context-Aware Prompt
   ↓
LLM Answer

---

## 🧪 Example API Usage

Request:
```json
{
  "question": "Tell me about GPT"
}
```

Response:
```json
{
  "answer": "GPT stands for Generative Pre-trained Transformer..."
}
```

Out-of-scope queries return:
```
Not found in document.
```
```
```

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
---


## ⚙️ Tech Stack

- FastAPI
- LangChain
- Astra DB / Cassandra
- EasyOCR (GPU)
- HuggingFace BGE
- Groq LLaMA

---
## 📦 Versioning

- **v1.0** — Text-only RAG with FastAPI deployment
- **v1.1 (done)** — Persistent FAISS index (save/load)
- **v1.2 (done)** — Dockerized deployment
- **v2.0 (done)** — Multimodal RAG (text + images)

---

## 📜 License
MIT

This project intentionally prioritizes **correct RAG behavior** over conversational fluency:
- The system answers **only when evidence exists**
- Otherwise, it explicitly refuses

This design mirrors real-world, production RAG systems used for enterprise and knowledge-grounded applications.
