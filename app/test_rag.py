from rag_chain import RAGCHAIN

rag = RAGCHAIN()

query = (
    "Which companies in this document work on AI models?"
    "Provide the list of companies with their respective AI models."

)

response = rag.run(query)
print(response)