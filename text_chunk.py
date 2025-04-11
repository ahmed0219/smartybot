import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def extract_and_chunk_pdf(file):
    reader = PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return chunks



def extract_and_chunk_pdfs_from_dir(directory_path):
    all_chunks = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "rb") as file:
                chunks = extract_and_chunk_pdf(file)
                all_chunks.extend(chunks)
    return all_chunks

