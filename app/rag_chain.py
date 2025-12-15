from app.llm import get_llm
from app.retriever import get_rertriever,build_vector_store
import os
from dotenv import load_dotenv
load_dotenv()
from app.reranker import BGECrossEncoder

HF_TOKEN = os.getenv("HF_TOKEN")

PROMPT_TEMPLATE = """
Answer the question using ONLY the context below.
If the answer is not present, say "Not found in document".

Context:
{context}

Question:
{question}

Answer (clear and concise):
"""

class RAGCHAIN:
    def __init__(self):
        self.vectordb = build_vector_store()
        self.retriever = get_rertriever(self.
        vectordb)
        self.llm = get_llm()
        self.reranker = BGECrossEncoder()
        

    def run(self, question: str):
        docs = self.retriever.invoke(question)

        if not docs:
            return "Not found in document"

        # Optional reranking
        reranked_docs = self.reranker.rerank(question, docs)

        if not reranked_docs:
            return "Not found in document"

        context = "\n\n".join(d.page_content for d in reranked_docs)

        prompt = PROMPT_TEMPLATE.format(
            context=context,
            question=question
        )

        raw = self.llm.invoke(prompt)

        if hasattr(raw, "content"):
            answer = raw.content
        elif isinstance(raw, list):
            answer = raw[0].get("generated_text", "")
        else:
            answer = str(raw)

        answer = answer.strip()

        if not answer:
            return "Not found in document"

        return answer


    
