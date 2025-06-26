
# Identity Verification System 

**Built by: CogniCode**  
**Type:** AI-Powered Web App | Flask Backend | OCR + Face Matching

---

##  Project Overview

This project is a **secure, AI-driven identity and age verification system** built for web applications. It extracts and analyzes identity details from a simulated **Identity proofs** and verifies the user’s **selfie** through facial recognition, assessing both **age eligibility (18+)** and **identity match confidence**.

Ideal for digital KYC, age-restricted content access, or any application where user identity validation is critical.

---

##  Key Features

-  **Document + Face Match** using DeepFace + Facenet  
-  **Date of Birth Extraction** via OCR and Regex  
-  **Blurriness & Lighting Feedback** for better image quality  
-  **Multi-language OCR** support (via Tesseract)  
-  **Structured JSON Response** with age, match confidence, and errors  
-  **User Consent & Form Validation** built-in  
-  **Temporary File Handling** for privacy and cleanup  
---
## Requirement 

- blinker==1.9.0
- click==8.2.1
- colorama==0.4.6 
- itsdangerous==2.2.0 
- Jinja2==3.1.6 
- MarkupSafe==3.0.2 
- packaging==25.0 
- pillow==11.2.1 
- pytesseract==0.3.13 
- Werkzeug==3.1.3 
- flask==2.3.2 
- flask-cors==3.0.10 
- deepface==0.0.79
- tensorflow==2.11.0 
- keras==2.11.0
- numpy==1.23.5
- opencv-python==4.7.0.72
---

##  Tech Stack

| Layer         | Tech Used                                       |
|--------------|-------------------------------------------------|
| **Frontend** | HTML5, JavaScript, CSS, Bootstrap ,Tailwind CSS             |
| **Backend**  | Flask (Python), OpenCV, Tesseract OCR, DeepFace |
| **AI Models**| Facenet (via DeepFace), MTCNN                   |

---

##  Workflow Overview

1. **User uploads identity proof image (.jpg/.png)**  
2. **System extracts DOB and photo**  
3. **User captures selfie via webcam**  
4. **Blurriness and brightness checks performed**  
5. **Facial similarity calculated using embeddings**  
6. **DOB parsed & age verified (18+ check)**  
7. **Custom confidence score calculated**  
8. **Result returned to frontend (pass/fail)**  

---

##  Face Verification Logic
The logic in the verify_faces() function is centered around using AI-based facial recognition to determine whether two images — one from an uploaded ID and one from a live-captured selfie — belong to the same person. The function begins by saving both uploaded images temporarily to the local disk. It then uses the DeepFace library, specifically the Facenet model combined with the MTCNN face detector, to extract facial embeddings from both images. These embeddings are high-dimensional vectors representing unique facial features. DeepFace calculates the cosine distance between the two vectors, which quantifies how similar the faces are — the smaller the distance, the more alike the faces. This distance is then converted into a confidence score using the formula (1 - distance) × 100. If this confidence score meets or exceeds a predefined threshold (set to 75% by default), the function concludes that the faces match. The result, including whether it’s a match, the confidence score, and the calculated distance, is returned as a dictionary. Finally, any temporary files are deleted, and in case of errors during processing, a clear error message is returned instead.
-  **Embedding Extraction** using Facenet  
-  **Cosine Distance** → `confidence = (1 - distance) * 100`  
-  **Match if Confidence ≥ 75%**

---


##  OCR (Text Extraction ) Logic
The logic combines image preprocessing, OCR, text cleaning, and regular expression-based pattern matching to extract the Date of Birth (DOB) from ID card images.

The code first takes in raw image bytes (e.g., from an uploaded Aadhar card), decodes and preprocesses the image using OpenCV techniques like resizing, grayscale conversion, median blurring, and thresholding to enhance OCR performance. It then uses the Tesseract OCR engine (configured to support multiple Indian languages) to extract text from the image. The text is cleaned using regex to retain only relevant characters such as Devanagari (Hindi) script, English letters, digits, and common punctuation. Once the text is cleaned, the extract_dob() function uses a comprehensive set of regular expressions to scan for common DOB patterns. These patterns account for different date formats (e.g., DD/MM/YYYY, 2 Jan 2004, 2004-01-02) and label variations like DOB, Date of Birth, or D.O.B. The first matched date is returned as the extracted DOB. This pipeline ensures high accuracy in identifying birth dates across multilingual and noisy document scans.
-  **Image Preprocessing with OpenCV** Enhances image quality using resizing, grayscale conversion, blurring, and thresholding to improve OCR accuracy.  
-  **Multilingual OCR with Tesseract** → Extracts text from the image using Tesseract configured for English and multiple Indian languages
  - Supported Languages:
    - Hindi
    - Bengali
    - Tamil
    - Telugu
    - Gujarati
    - Marathi
    - Punjabi
    - Kannada

-  **DOB Pattern Matching with Regular Expressions** Uses a variety of regex patterns to detect and extract dates in different formats (e.g., DD/MM/YYYY, 2 Jan 2004, etc.) from the OCR text.

---

## 📦 Output Format (JSON Example)

```json
{
  "ocr_text": "...",
  "is_18_plus": true,
  "face_match_confidence": 84.7,
  "face_match_result": "Matched",
  "errors": null
}
```
---
##  Use Cases

This system can be applied across multiple real-world scenarios where identity and age verification are crucial:

-  **Digital KYC (Know Your Customer)** for financial apps and fintech onboarding  
-  **Legal Age Verification** for platforms offering alcohol, tobacco, or age-restricted content  
-  **E-learning & Exams** to verify student identity during remote tests or admissions  
-  **Online Gaming Platforms** to restrict access to adult content or age-sensitive features  
-  **Healthcare Platforms** for verifying patient identity during telemedicine sessions  
-  **E-Governance Portals** where secure document validation is necessary  

---

##  Future Scope

This project lays the foundation for a robust AI-based identity verification framework. Potential future enhancements include:

-  **Mobile App Integration** for native Android/iOS capture and verification  
-  **Support for Multiple Document Types** like PAN, Passport, Driver’s License  
-  **Liveness Detection** to prevent spoofing with photos or videos  
-  **Improved OCR for Regional Languages** using advanced NLP post-processing  
-  **Encrypted Identity Storage** with blockchain or secure vaults  
-  **API-as-a-Service** to let other apps integrate this verification as a module  
-  **Admin Dashboard** for analytics and audit trail of verifications

---

## 🚀 How to Run This Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Srishhttiii/Identity-Verification-System.git
cd Identity-Verification-System
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

### 3. Activate the Environment

**On Windows:**
```bash
myenv\Scripts\activate
```

**On macOS/Linux:**
```bash
source myenv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python main.py
```

### 6. Open your Browser

Visit: [http://localhost:5000](http://localhost:5000)

---

## 📂 Demo & Presentation

You can view the complete presentation deck and demo video here:  
👉 [Google Drive Folder](https://drive.google.com/drive/folders/1nOFM6RIINTnsKxvS3o98KzOZd0rKXHT1?usp=sharing)

