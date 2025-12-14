from app.evaluation.relevance import relevance_score
from app.evaluation.faithfullness import faithfulness_score
from app.evaluation.eval_data import EVAL_QUESTIONS
from app.evaluation.relevance import relevance_score
from app.rag_chain import RAGCHAIN

rag = RAGCHAIN()

for item in EVAL_QUESTIONS:
    question = item["question"]
    expected_keywords = item["expected_keywords"]

    answer = rag.run(question)


    f_score = faithfulness_score(answer,context=question)
    r_score = relevance_score(answer,expected_keywords)

    print("=" * 50)
    print("Q:", question)
    print("A:", answer)
    print(f"Faithfulness: {f_score:.2f}")
    print(f"Relevance: {r_score:.2f}")

