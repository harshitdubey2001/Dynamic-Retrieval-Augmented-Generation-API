from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv("HF_TOKEN")

def get_text_embeddings():
    
    return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")