from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from app.hybrid_rag import HybridRAG

app = FastAPI(
    title="Dynamic Multimodal RAG API (v2)",
    description="Hybrid RAG with text + image grounding",
    version="2.0.0",
)

rag = HybridRAG()

class QueryRequest(BaseModel):
    question:str

class Source(BaseModel):
    file: Optional[str]
    page: Optional[int]
    modality: Optional[str]    

class QueryResponse(BaseModel):
    answer:str
    sources: List[Source]


    


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = rag.run(req.question)
    return result

