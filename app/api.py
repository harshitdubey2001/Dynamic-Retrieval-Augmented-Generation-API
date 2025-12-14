from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_chain import RAGCHAIN

app = FastAPI(
    title="RAG API",
    description="Dynamic Retrieval-Augmented Generation API",
    version="0.1.0",
)

# LOAD RAG
rag = RAGCHAIN()

class QueryRequest(BaseModel):
    question:str

class QueryResponse(BaseModel):
    answer:str

@app.get("/health")
def health():
    return {"status":"ok"}


@app.post("/query",response_model=QueryResponse)
def query(request:QueryRequest):
    answer = rag.run(request.question)
    return QueryResponse(answer=answer)