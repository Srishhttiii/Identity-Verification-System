import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime


# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(file_bytes):  #Takes raw image bytes (from an uploaded file) and returns extracted, cleaned text using OCR.
    # Decode image
    img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")


    # Preprocess for OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) ## Scaling up image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converting to grayscale
    gray = cv2.medianBlur(gray, 3) # Reducing noise while keeping edges sharp
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # Apply binary inverse thresholding


    thresh = cv2.bitwise_not(thresh)  # Flip black/white to make text black on white


    # OCR using Tesseract
    custom_config = r'--oem 3 --psm 4 -l eng+hin+tam+ben+guj+pan+mar+tel+kan'
    # --oem 3: Use the default OCR Engine Mode (neural nets + legacy)
    # --psm 4: Assume a single column of text in variable sizes
    # -l eng+hin: OCR in both English and Hindi languages


    text = pytesseract.image_to_string(thresh, config=custom_config)   # Performing OCR on the thresholded image


    # Clean extracted text
    cleaned_lines = []
    for line in text.split('\n'):


        # we want to keep only English, Hindi characters, numbers, and some punctuations
        line = re.sub(r'[^\u0900-\u097F A-Za-z0-9:/\-\s,.]', '', line)
        if line.strip(): # Skip empty lines
            cleaned_lines.append(line)


    # Join cleaned lines into a single string
    cleaned_text = "\n".join(cleaned_lines)


    return cleaned_text  # Return final cleaned text




def extract_dob(text):
# Takes OCR text and tries to find a valid date of birth (DOB) using multiple regular expression patterns.
   
   
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
    # Go through each pattern and return the first matched date
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"✅ Pattern matched: {pattern}")
            print(f"🎯 Extracted DOB: {match.group(1) if match.lastindex else match.group()}")
            return match.group(1) if match.lastindex else match.group()


    print("❌ No pattern matched.")
    return None





