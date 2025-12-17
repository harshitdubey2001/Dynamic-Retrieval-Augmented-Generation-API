import os

from pathlib import Path

from .image_ingestion import ingest_image
IMAGE_DIR = Path(__file__).resolve().parents[1] / "data" / "images"

def build_image_documents():
    docs = []

    if not IMAGE_DIR.exists():
        print(f"[WARN] Image directory does not exist: {IMAGE_DIR}")

    for img_path in IMAGE_DIR.iterdir():
        if img_path.suffix.lower() not in (".jpg", ".png", ".jpeg"):
            continue

        
        doc = ingest_image(str(img_path))

        if doc:
            docs.append(doc)
    print(f"[INFO] Ingested {len(docs)} image documents")
    return docs        
       