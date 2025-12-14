import re

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

def normalize(text:str)->set:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return set(text.split())





def faithfulness_score(answer, context) -> float:
    """
    Measures how much of the answer is grounded in context.
    """
    answer = _to_text(answer)
    context = _to_text(context)
    answer_tokens = normalize(answer)
    context_tokens = normalize(context)

    if not answer_tokens:
        return 0.0

    supported = answer_tokens & context_tokens
    return len(supported) / len(answer_tokens)
