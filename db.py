import chromadb
DB_NAME = "white_papers1"

def get_db():
    chroma_client = chromadb.PersistentClient(path="./newchroma_db")
    db = chroma_client.get_collection(name=DB_NAME)
    return db
