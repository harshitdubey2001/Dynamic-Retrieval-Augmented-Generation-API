from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
import cassio
astra_application_token = os.getenv("ASTRA_DB_APPICATION_TOKEN")

astra_db_id = os.getenv("ASTRA_DB_ID")

cassio.init(token=astra_application_token,database_id=astra_db_id)

HF_TOKEN = os.getenv("HF_TOKEN")

APP_DIR= Path(__file__).resolve().parent
DOC_DIR = APP_DIR/"data"/"docs"

INGESTED_MARKER = "v1_ingested"

def build_vector_store(path:Path = DOC_DIR):
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    embdeddings = HuggingFaceEmbeddings(
        model="BAAI/bge-base-en-v1.5"
    )

    vectordb = Cassandra(
        embedding=embdeddings,
        table_name="rag_documents",
        keyspace=None

    )
   
    loader = DirectoryLoader(
            str(path),
            glob="**/*.txt",
            loader_cls=TextLoader,
            
        )

    docs = loader.load()

    
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

    chunks = splitter.split_documents(docs)
    

    if not chunks:
            raise ValueError("No chunks created. Documents may be empty.")
        
    vectordb.add_documents(chunks)
    print(f"Generated & stored {len(chunks)} chunks")


    return vectordb


def get_retriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": 10})
        


    







    
    return vectordb


def get_rertriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": 10})


