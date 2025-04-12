import chromadb
import chromadb
from GeminiEmbeddingFunction import GeminiEmbeddingFunction
DB_NAME = "white_papers_db"

def get_db():
    embed_fn = GeminiEmbeddingFunction()
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    db = chroma_client.get_collection(name="white_papers_db", embedding_function=embed_fn)
    return db
