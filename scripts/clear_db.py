from retrievers.text_retriever import build_text_vector_store

vs = build_text_vector_store()
vs.clear()
print("Vector store cleared")