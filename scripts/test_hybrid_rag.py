from app.hybrid_rag import HybridRAG

def main():
    rag = HybridRAG()

    question = "Tell me about GPT"

    answer = rag.run(question)

    print("\nAnswer\n",answer)

if __name__ == "__main__": 
    main()    