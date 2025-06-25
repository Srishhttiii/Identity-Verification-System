import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(file_bytes):
    # Decode image
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")

    # Preprocess for OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.bitwise_not(thresh)

    # OCR using Tesseract
    custom_config = r'--oem 3 --psm 4 -l eng+hin'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    # Clean extracted text
    cleaned_lines = []
    for line in text.split('\n'):
        line = re.sub(r'[^\u0900-\u097F A-Za-z0-9:/\-\s,.]', '', line)
        if line.strip():
            cleaned_lines.append(line)
    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text


def extract_dob(text):
    # Date patterns
    date_patterns = [
        # Multi-line or space-separated DOB labels
        r'DATE OF BIRTH[:\- ]*\n?(\d{2}[/-]\d{2}[/-]\d{4})',
        r'Date of Birth[:\- ]*\n?(\d{2}[/-]\d{2}[/-]\d{4})',
        r'D.O.B[:\- ]*\n?(\d{2}[/-]\d{2}[/-]\d{4})',
        r'DOB[:\- ]*\n?(\d{2}[/-]\d{2}[/-]\d{4})',

        # Text month formats
        r'DOB[:\- ]*\n?(\d{1,2} [A-Za-z]{3,9},? \d{4})',
        r'DATE OF BIRTH[:\- ]*\n?(\d{1,2} [A-Za-z]{3,9},? \d{4})',
        r'Date of Birth[:\- ]*\n?(\d{1,2} [A-Za-z]{3,9},? \d{4})',

        # Without labels
        r'\b\d{1,2} [A-Za-z]{3,9},? \d{4}\b',
        r'\b\d{2}[A-Za-z]{3}\d{4}\b',
        r'\b\d{2} [A-Za-z]{3} \d{4}\b',
        r'\b\d{2}\s?[A-Za-z]{3}\s?\d{4}\b',

        # Pure numeric dates
        r'\b\d{2}[/-]\d{2}[/-]\d{4}\b',
        r'\b\d{4}[/-]\d{2}[/-]\d{2}\b',
        r'\b\d{2}[.]\d{2}[.]\d{4}\b'
    ]

    # Try matching date
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1) if match.lastindex else match.group()
    return None