import json
import os
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "images"

CACHE_DIR.mkdir(exist_ok=True)
CACHE_PATH = CACHE_DIR / "image_text_cache.json"

def load_cache():
    if not CACHE_PATH.exists():
        return {}
    with open(CACHE_PATH,"r") as f:
        return json.load(f)
    
def save_cache(cache):
    with open(CACHE_PATH,"w") as f:
        json.dump(cache,f,indent=2)    