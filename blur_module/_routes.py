from flask import Blueprint, request, jsonify
from blur_module.blur_backend import analyze_image
import tempfile
import os

blur_bp = Blueprint('blur', __name__)


@blur_bp.route('/check-image-blur', methods=['POST'])
def check_image_blur():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files.get('image')
    if not file or file.filename == '':
        return jsonify({"error": "No image received"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_path = temp_file.name
        file.save(temp_path)

    lap_var, brightness, blur_status, light_status = analyze_image(temp_path)
    os.remove(temp_path)

    if lap_var is None:
        return jsonify({'error': 'Invalid image'}), 400

    return jsonify({
        "laplacian_variance": lap_var,
        "brightness": brightness,
        "blur_status": blur_status,
        "light_status": light_status
    })



