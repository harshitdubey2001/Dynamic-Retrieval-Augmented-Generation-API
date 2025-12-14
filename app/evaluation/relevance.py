from sentence_transformers import util,SentenceTransformer
import torch

_model = SentenceTransformer('all-MiniLM-L6-v2',device="cpu")

def _to_text(x):
    """
    Robustly normalize LLM outputs to string.
    Handles:
    - str
    - list[str]
    - list[dict]
    """
    if isinstance(x, str):
        return x

    if isinstance(x, list) and len(x) > 0:
        first = x[0]

        if isinstance(first, dict):
            return first.get("generated_text", "")

        if isinstance(first, str):
            return first

    return str(x)

def relevance_score(answer,context)->float:

    answer = _to_text(answer)
    context = _to_text(context)
    if not answer.strip() or not context.strip():
        return 0.0
    
    emb_answer = _model.encode(answer,convert_to_tensor=True)
    emb_context = _model.encode(context,convert_to_numpy=True)

    return float(util.cos_sim(emb_answer,emb_context))
