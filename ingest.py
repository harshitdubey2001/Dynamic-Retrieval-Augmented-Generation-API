from retrievers.text_retriever import build_text_vector_store
from embeddings.text_embeddings import get_text_embeddings
from embeddings.image_embeddings import build_image_documents
from app.llm import get_llm
from embeddings.text_ingestion import load_text_documents
from embeddings.pdf_ingestion import ingest_pdf
from pathlib import Path
PDF_DIR = Path("data/pdfs")
PDF_IMAGE_DIR = Path("data/pdf_images")

def run_ingestion():
    vectorstore = build_text_vector_store()

    text_docs = load_text_documents()
    image_docs = build_image_documents()
    pdf_docs = []
    for pdf in PDF_DIR.glob("*.pdf"):
        pdf_docs.extend(ingest_pdf(str(pdf),PDF_IMAGE_DIR))

    print(f"Text docs: {len(text_docs)}")
    print(f"Image docs: {len(image_docs)}")
    print(f"PDF docs: {len(pdf_docs)}")

    all_docs =text_docs + image_docs + pdf_docs
    vectorstore.add_documents(all_docs)

    print(f"[INGEST]Stored {len(all_docs)} Total documents")

if __name__ == "__main__":
    run_ingestion()    