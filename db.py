import chromadb
DB_NAME = "white_papers_db"

def get_db():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    db = chroma_client.get_collection(name=DB_NAME)
    return db
