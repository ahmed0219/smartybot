from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
def extract_and_chunk_pdf(file):
    reader = PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return chunks