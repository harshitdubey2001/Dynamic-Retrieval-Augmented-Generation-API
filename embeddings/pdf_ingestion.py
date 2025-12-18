from langchain_classic.schema import Document
from pathlib import Path
from embeddings.pdf_loader import extract_image_from_pdf,extract_pdf_text
from embeddings.image_ingestion import ingest_image

def ingest_pdf(pdf_path: str, image_output_dir: Path):
    documents = []

    #Text pages
    text_pages = extract_pdf_text(pdf_path)
    for page in text_pages:
        documents.append(
            Document(
                page_content=page["text"],
                metadata={
                    "source":pdf_path,
                    "page":page["page"],
                    "modality":"pdf_text"
                }
            )
        )
        
    # Images inside pdf
    image_paths = extract_image_from_pdf(pdf_path,image_output_dir)  
    for img_path in image_paths:
        img_doc = ingest_image(img_path)
        if img_doc:
            img_doc.metadata['source_pdf']=pdf_path
            img_doc.metadata["modality"]="pdf_image"
            documents.append(img_doc)
    return documents        