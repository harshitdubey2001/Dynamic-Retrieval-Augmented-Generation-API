import os
import cassio
from dotenv import load_dotenv
load_dotenv()
from langchain_community.vectorstores import Cassandra
from langchain_core.embeddings import Embeddings

class PrecomputedImageEmbeddings(Embeddings):
    DIMENSION = 512

    def embed_documents(self, texts):
        return texts

    def embed_query(self, text):
        return [0.0] * self.DIMENSION

cassio.init(
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    database_id=os.getenv("ASTRA_DB_ID"),
)

def clear_image_table():
    vectorstore = Cassandra(
        embedding=PrecomputedImageEmbeddings(),
        table_name="rag_image_documents",
        keyspace=None
    )

    # Clear or delete
    if hasattr(vectorstore, "clear"):
        vectorstore.clear()
        print("Image table cleared")
    else:
        vectorstore.delete_collection()
        print("Image table deleted")

if __name__ == "__main__":
    clear_image_table()