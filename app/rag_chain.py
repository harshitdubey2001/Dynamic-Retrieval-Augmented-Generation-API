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
        

    def run(self,question:str):
        docs = self.retriever._get_relevant_documents(question,run_manager=None)

        reranked_docs = self.reranker.rerank(question,docs)

        context = "\n\n".join([d.page_content for d in reranked_docs])

        if len(context.strip()) < 50:
           return "Not found in document"
        
        from app.evaluation.relevance import relevance_score
        sim = relevance_score(question, context)

        ABSTRACT_TRIGGERS = (
                "what types",
                "what kind",
                "what categories",
                "summarize",
                "overview",
                "describe"
            )

        is_abstract = any(t in question.lower() for t in ABSTRACT_TRIGGERS)

        if not is_abstract and sim < 0.35:
                return "Not found in document"

        prompt = PROMPT_TEMPLATE.format(context=context,question=question)


        raw = self.llm.invoke(prompt)

        if isinstance(raw,list):
            answer = raw[0].get("generated_text", "")
        else:
            answer = str(raw)    

        return answer.strip()
    
    
