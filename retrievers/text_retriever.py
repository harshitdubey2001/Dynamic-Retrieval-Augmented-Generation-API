import os
import cassio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Cassandra

from langchain_core.documents import Document

from embeddings.text_embeddings import get_text_embeddings

DOCS_DIR = Path(__file__).resolve().parents[1] / "data" / "docs"

def init_cassandra():
    token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    db_id = os.getenv("ASTRA_DB_ID")

    cassio.init(
        token=token,
        database_id=db_id,
    )

def build_text_vector_store():
    init_cassandra()

    embeddings= get_text_embeddings()
        
    return Cassandra(
        embedding=embeddings,
        table_name="rag_documents",
        keyspace=None,
    )

def get_text_retriever(k=5):
    vectorstore = build_text_vector_store()
    return vectorstore.as_retriever(search_kwargs={"k": k})   


