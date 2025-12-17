from retrievers.text_retriever import get_text_retriever
from app.llm import get_llm
from app.reranker import LLMReranker


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

        if not docs:
            return {"answer": "Not found in document."}
        
        docs =  self.reranker.rerank(question,docs)

        context = "\n\n".join(d.page_content for d in docs)

        keyword_mode = is_keyword_heavy(context)

        if keyword_mode:
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
        else:
            prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say "Not found in document".

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)
        answer = response.content.strip() if hasattr(response, "content") else str(response).strip()

        return {"answer": answer}
