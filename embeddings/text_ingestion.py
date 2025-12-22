from pathlib import Path
import os
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from cache.ingestion import compute_hash,load_registry,save_registry
DOCS_DIR = Path(__file__).resolve().parents[1] / "data" / "docs"

def load_text_documents():
    

    registry = load_registry()
    new_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    for file in DOCS_DIR.glob("*.txt"):
        path = str(file)
        file_hash = compute_hash(path)

        if registry.get(path)== file_hash:
            print(f"[INFO] Text already ingested:{path}")
            continue
        loader = TextLoader(path,encoding="utf-8")
        docs = loader.load()

        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata.update({
                "file_name": os.path.basename(path),
                "source":path,
                "modality":"text",
                "source_type": "text"
            })


            new_chunks.extend(chunks)

            registry[path]= file_hash
            print(f"[INFO] Text Updated: {path}")
    save_registry(registry)        
    
    return new_chunks
