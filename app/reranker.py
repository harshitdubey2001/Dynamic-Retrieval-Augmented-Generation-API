from typing import List
from langchain_core.documents import Document

class LLMReranker:
    def __init__(self,llm,top_n: int = 3):
        self.llm =llm
        self.top_n = top_n


    def rerank(self, question: str, docs: List[Document]) -> List[Document]:
        if not docs:
            return []
        
        blocks = []
        for i,d in enumerate(docs):
            blocks.append(
                f"[{i}]{d.page_content.strip()[:400]}"
            )

        prompt = f"""
You are a relevance ranking system.

Given a question and a list of documents, select the document numbers
that are MOST relevant to answering the question.

Rules:
- Use ONLY the given documents
- Do NOT add new information
- Return ONLY a comma-separated list of document numbers
- Order them from most to least relevant

Question:
{question}

Documents:
{chr(10).join(blocks)}

Relevant document numbers:
"""    

        response = self.llm.invoke(prompt)
        raw = response.content.strip() if hasattr(response,"content") else str(response)

        try:
            indices = [int(i.strip())for i in raw.split()(",")]
        except Exception:

            return docs[:self.top_n]

        ranked = [docs[i]for i in indices if i < len(docs)]
        return ranked[:self.top_n]    