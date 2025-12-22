from langchain_classic.schema import Document
from pathlib import Path
import os
import re
from embeddings.pdf_loader import extract_image_from_pdf,extract_pdf_text
from embeddings.image_ingestion import ingest_image
from cache.ingestion import load_registry,save_registry,compute_hash

def _extract_page_from_filename(filename: str):
    """
    page_12_img_0.png → 12
    """
    match = re.search(r"page_(\d+)", filename)
    return int(match.group(1)) if match else None



def ingest_pdf(pdf_path: str, image_output_dir: Path):

    registry = load_registry()
    documents = []

    pdf_path = str(pdf_path)
    pdf_hash =compute_hash(pdf_path)

    if registry.get(pdf_path)==pdf_hash:
        print(f"[INFO] PDF already ingested {pdf_path}")
        return []
    
    pdf_name = os.path.basename(pdf_path)

    #Text pages
    text_pages = extract_pdf_text(pdf_path)
    for page in text_pages:
        documents.append(
            Document(
                page_content=page["text"],
                metadata={
                    "file_name": pdf_name,
                    "page": int(page["page"]),
                    "modality":"pdf_text",
                    "source_type": "pdf"
                }
            )
        )
        
    # Images inside pdf
    image_paths = extract_image_from_pdf(pdf_path,image_output_dir)  
    for img_path in image_paths:
        img_doc = ingest_image(img_path)

        page_num = _extract_page_from_filename(os.path.basename(img_path))
        if img_doc:
            img_doc.metadata.update({
                "file_name": pdf_name,
                "page": page_num,
                "image_file": os.path.basename(img_path),  
                "modality": "pdf_image",
                "source_type": "pdf"
                })
            documents.append(img_doc)

    registry[pdf_path]=pdf_hash
    save_registry(registry)

    print(f"[INGEST] PDF updated:{pdf_path} ({len(documents)} docs)")        
    return documents        