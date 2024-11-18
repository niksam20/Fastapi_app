import pdfplumber
import pytesseract
from PIL import Image

def save_uploaded_file(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image file."""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)
    

