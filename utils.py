from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return ''.join(page.extract_text() or '' for page in reader.pages)
