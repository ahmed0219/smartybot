import os
from text_chunk import extract_and_chunk_pdfs_from_dir
from GeminiEmbeddingFunction import GeminiEmbeddingFunction
import chromadb

# === CONFIGURATION ===
DB_NAME = "white_papers1"
PDF_DIR = "pdf"  # your folder of PDFs
# === INIT EMBEDDING FUNCTION ===
embed_fn = GeminiEmbeddingFunction()
embed_fn.document_mode = True

# === INIT CHROMADB ===
try:
    chroma_client = chromadb.PersistentClient(path="./newchroma_db")
    db = chroma_client.create_collection(name=DB_NAME, embedding_function=embed_fn)
    print(f"✅ Collection '{DB_NAME}' initialized.")
except Exception as e:
    print(f"❌ Error initializing ChromaDB: {e}")
    raise

# === CHUNK AND EMBED ===
try:
    print("⏳ Extracting and chunking PDFs...")
    documents = extract_and_chunk_pdfs_from_dir(PDF_DIR)
    ids = [f"doc_{i}" for i in range(len(documents))]
    db.add(documents=documents, ids=ids)
    print(f"✅ {len(documents)} chunks added to the DB.")
except Exception as e:
    print(f"❌ Error processing documents: {e}")
    raise
