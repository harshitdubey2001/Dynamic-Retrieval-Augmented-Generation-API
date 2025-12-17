from retrievers.text_retriever import build_text_vector_store
from embeddings.text_embeddings import get_text_embeddings
from embeddings.image_embeddings import build_image_documents
from app.llm import get_llm
from embeddings.text_ingestion import load_text_documents

def run_ingestion():
    llm =get_llm()
    vectorstore = build_text_vector_store()

    text_docs = load_text_documents()
    image_docs = build_image_documents()

    print(f"Text docs: {len(text_docs)}")
    print(f"Image docs: {len(image_docs)}")

    all_docs =text_docs + image_docs
    vectorstore.add_documents(all_docs)

    print(f"[INGEST]Stored {len(all_docs)} Total documents")

if __name__ == "__main__":
    run_ingestion()    