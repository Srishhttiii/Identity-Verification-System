# ocr_module/routes.py

from flask import Blueprint, request, jsonify
from backend_ocr import extract_text_from_image, extract_dob
from datetime import datetime

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/extract', methods=['POST'])
def extract():
    try:
        image_file = request.files.get('aadhar')
        if not image_file:
            return jsonify({'error': 'No Aadhar image uploaded'}), 400
        
        print(f"📥 File received: {image_file.filename}")
        print(f"📦 File type: {image_file.content_type}")

        file_bytes = image_file.read()

        try:
            text = extract_text_from_image(file_bytes)
        except Exception as e:
            print("❌ OCR error:", e)
            return jsonify({'error': f"OCR Failed: {str(e)}"}), 500

        dob = extract_dob(text)

        age = None
        is_18_plus = None
        if dob:
            for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y', '%d %b %Y', '%d %B %Y']:
                try:
                    dob_date = datetime.strptime(dob, fmt)
                    today = datetime.today()
                    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                    is_18_plus = age >= 18
                    break
                except ValueError as err:
                    print(f"⚠️ Date format issue: {err}")

        return jsonify({
            'raw_text': text,
            'dob': dob,
            'age': age,
            'is_18_plus': is_18_plus
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
