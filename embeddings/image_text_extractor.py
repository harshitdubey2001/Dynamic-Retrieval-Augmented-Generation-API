from PIL import Image,ImageOps
import numpy as np
import os
import easyocr

import easyocr

# Initialize once (important)
reader = easyocr.Reader(['en'], gpu=True)

def extract_text_from_image(image_path: str) -> str:

    try:
        results = reader.readtext(image_path)
        texts = [text for (_, text, conf) in results if text.strip()]
        return "\n".join(texts)

    except Exception as e:
        print(f"[OCR ERROR] {image_path}: {e}")
        return ""
        

