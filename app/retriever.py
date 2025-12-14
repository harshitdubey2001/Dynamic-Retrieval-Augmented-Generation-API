from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

APP_DIR= Path(__file__).resolve().parent
DOC_DIR = APP_DIR/"data"/"docs"

def build_vector_store(path:Path = DOC_DIR):
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    

    loader = DirectoryLoader(str(path),glob="**/*.txt")
    docs = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("No chunks created. Documents may be empty.")


    print("Generated chunks",len(chunks))

    embdeddings = HuggingFaceEmbeddings(
        model="BAAI/bge-base-en-v1.5"
    )

    vectordb = FAISS.from_documents(chunks, embdeddings)

    return vectordb


def get_rertriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": 10})


