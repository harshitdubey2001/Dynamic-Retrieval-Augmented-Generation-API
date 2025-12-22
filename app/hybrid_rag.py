from retrievers.text_retriever import get_text_retriever
from app.llm import get_llm
from app.reranker import LLMReranker

import os
import re

def extract_sources(docs, max_sources=5):
    sources = []
    seen = set()

    for d in docs:
        meta = d.metadata or {}

        file_name = meta.get("file_name")
        modality = meta.get("modality")

        raw_page = meta.get("page")
        page = None

        if raw_page is not None:
            if isinstance(raw_page, int):
                page = raw_page
            elif isinstance(raw_page, str):
                try:
                    page = int(float(raw_page))
                except ValueError:
                    page = None

        key = (file_name, page, modality)
        if key in seen:
            continue
        seen.add(key)

        sources.append({
            "file": file_name,
            "page": page,
            "modality": modality
        })

        if len(sources) >= max_sources:
            break

    return sources




def is_keyword_heavy(text: str) -> bool:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    short_lines = [l for l in lines if len(l.split()) <= 3]
    return len(short_lines) >= max(3, len(lines) // 2)


class HybridRAG:
    def __init__(self):
        self.retriever = get_text_retriever(k=8)
        self.llm = get_llm()
        self.reranker = LLMReranker(self.llm,top_n=3)

    def run(self, question: str):
        docs = self.retriever.invoke(question)

        top_modality = docs[0].metadata.get("modality")
        if top_modality == "image":
            docs = [d for d in docs if d.metadata.get("modality") == "image"]

        if top_modality == "pdf_text":
            docs = [d for d in docs if d.metadata.get("modality") == "pdf_text"]

        if top_modality == "pdf_image": 
            docs = [d for d in docs if d.metadata.get("modality") == "pdf_image"]        

        if not docs:
            return {"answer": "Not found in document."}
        
        docs =  self.reranker.rerank(question,docs)

        context = "\n\n".join(d.page_content for d in docs)

        keyword_mode = is_keyword_heavy(context)

        sources = extract_sources(docs)

        if keyword_mode:
            prompt = f"""
You are answering questions using retrieved context.

The context may come from OCR of images or diagrams.
OCR text may be fragmented labels, not full sentences.

Rules:
- Use ONLY the provided context.
- Do NOT use outside knowledge.
- If the context contains labels or components, you may describe or summarize them.
- If the order or relationships are implied by labels (e.g., pipeline steps), you may infer a reasonable sequence.
- If the context truly lacks relevant information, say "Not found in document".

Context:
{context}

Question:
{question}

Answer:
"""
        else:
            prompt = f"""
You are given extracted context that may consist of keywords or labels.

Rules:
- If the context lists components or steps as keywords, list them clearly.
- Do NOT add information not present.
- If no relevant keywords exist, say "Not found in document".


Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)
        answer = response.content.strip() if hasattr(response, "content") else str(response).strip()

        return {
            "answer": answer,
            "sources": sources
            }
