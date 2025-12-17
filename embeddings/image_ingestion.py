from .image_cache import load_cache,save_cache
from embeddings.image_text_extractor import extract_text_from_image
import os
from langchain_classic.schema import Document

def ingest_image(image_path):

    cache = load_cache()

    key = os.path.abspath(image_path)

    if key in cache:
        text = cache[key]
    else:
        text = extract_text_from_image(image_path)

    if text and len(text.strip())>=20:
        cache[key]=text
        save_cache(cache)

    if not text or len(text.strip())<20:
        print(f"[INFO] Image skipped (no usbale text): {image_path}")
        return None    

    return Document(
    page_content=text,
    metadata={
        "source": image_path,
        "filename": os.path.basename(image_path),
        "modality": "image"
    }
)       