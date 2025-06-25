from flask import Flask, request, jsonify, render_template
import os
import cv2
import tempfile

app = Flask(__name__)

# Directory where uploaded files will temporarily be stored
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Function to detect blur and categorize
def detect_blur_category(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Invalid image"

    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()

    if laplacian_var >= 100:
        status = "Clear"
    elif laplacian_var >= 50:
        status = "Moderate"
    else:
        status = "Blurry"

    return laplacian_var, status


@app.route('/')
def index():
    return render_template('front.html')


@app.route('/check-image-blur', methods=['POST'])
def check_image_blur():
    try:
        file = request.files.get('image')
        if not file or file.filename == '':
            return jsonify({"error": "No image received"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)

        lap_var, blur_status = detect_blur_category(temp_path)
        os.remove(temp_path)

        if lap_var is None:
            return jsonify({'error': 'Invalid image'}), 400

        return jsonify({
            "laplacian_variance": round(lap_var, 2),
            "status": blur_status
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)