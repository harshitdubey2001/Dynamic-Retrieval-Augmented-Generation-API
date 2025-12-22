import json
import hashlib
from pathlib import Path

REGISTRY_PATH = Path("cache/ingestion_registry.json")

def compute_hash(path: str)->str:
    h = hashlib.md5()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_registry()->dict:
    if not REGISTRY_PATH.exists():
        return {}
    try:
        return json.loads(REGISTRY_PATH.read_text())
    except Exception:
        return {}


def save_registry(registry: dict):
    REGISTRY_PATH.parent.mkdir(exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry,indent=2))            