from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path, chunk_size=300):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    # chunk text
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks