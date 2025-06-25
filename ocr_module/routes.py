from flask import Blueprint, request, jsonify
from backend_ocr import extract_text_from_image, extract_dob
from datetime import datetime

ocr_bp = Blueprint('ocr', __name__)

def parse_dob(dob_str):
    """Try multiple date formats to convert extracted DOB string into a datetime object."""
    date_formats = [
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d %b %Y',
        '%d %B %Y'
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(dob_str, fmt)
        except ValueError:
            continue
    return None

@ocr_bp.route('/extract', methods=['POST'])
def extract():
    try:
        aadhar_file = request.files.get('aadhar')
        selfie_file = request.files.get('selfie')

        if not aadhar_file:
            return jsonify({'error': 'No Aadhar image uploaded'}), 400
        if not selfie_file:
            return jsonify({'error': 'No selfie image uploaded'}), 400

        print(f"📥 Aadhar received: {aadhar_file.filename}")
        print(f"📸 Selfie received: {selfie_file.filename}")

        aadhar_bytes = aadhar_file.read()

        try:
            text = extract_text_from_image(aadhar_bytes)
        except Exception as e:
            print("❌ OCR error:", e)
            return jsonify({'error': f"OCR Failed: {str(e)}"}), 500

        dob = extract_dob(text)
        age = None
        is_18_plus = None

        if dob:
            dob_date = parse_dob(dob)
            if dob_date:
                today = datetime.today()
                age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                is_18_plus = age >= 18
            else:
                print(f"⚠️ Unable to parse DOB format: {dob}")

        return jsonify({
            'raw_text': text,
            'dob': dob,
            'age': age,
            'is_18_plus': is_18_plus,
            'selfie_uploaded': selfie_file.filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
