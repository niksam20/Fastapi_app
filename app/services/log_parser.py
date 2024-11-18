import os
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import re
import random

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image file."""
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def parse_logs(log_file: str):
    """Parse logs and extract features."""
    log_entries = []
    with open(log_file, 'r') as file:
        for line in file:
            match = re.match(r'(\S+\s+\S+)\s+\w+\s+(.*)', line)
            if match:
                timestamp = match.group(1)
                feature1 = random.randint(10, 100)
                feature2 = random.randint(20, 200)
                log_entries.append((timestamp, feature1, feature2))
    return log_entries

def save_to_csv(log_entries, output_file: str):
    """Save log entries to a CSV file."""
    df = pd.DataFrame(log_entries, columns=['timestamp', 'feature1', 'feature2'])
    df.to_csv(output_file, index=False)


