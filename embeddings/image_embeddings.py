import os

from pathlib import Path

from cache.ingestion import load_registry,compute_hash,save_registry

from .image_ingestion import ingest_image
IMAGE_DIR = Path(__file__).resolve().parents[1] / "data" / "images"

def build_image_documents():
    registry = load_registry()
    new_docs = []

    if not IMAGE_DIR.exists():
        print(f"[WARN] Image directory does not exist: {IMAGE_DIR}")

    for img_path in IMAGE_DIR.iterdir():
        if img_path.suffix.lower() not in (".jpg", ".png", ".jpeg"):
            continue

        path = str(img_path)
        file_hash = compute_hash(path)

        if registry.get(path)==file_hash:
            print(f"[SKIP] Image already ingested: {path}")
            continue

        
        doc = ingest_image(str(img_path))

        if doc:
            new_docs.append(doc)
            registry[path]= file_hash
            print(f"[INFO] Image updated:{path}")
        else:
            print(f"[SKIP] Image has no usable text: {path}")    

        save_registry(registry)
        print(f"[INFO] Ingested {len(new_docs)}new image documents")
    return new_docs        
       