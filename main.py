import chromadb
from GeminiEmbeddingFunction import GeminiEmbeddingFunction  # if needed

DB_NAME = "white_papers_db"
CHROMA_PATH = "./chroma_db"


def get_db():
    embed_fn = GeminiEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    db = chroma_client.get_collection(name="white_papers_db", embedding_function=embed_fn)
    return db


if __name__ == "__main__":
    db = get_db()

    # Example query
    query = "What is LLM?"
    result = db.query(query_texts=[query], n_results=3)

    for i, doc in enumerate(result["documents"][0]):
        print(f"📄 Result {i+1}: {doc}")
