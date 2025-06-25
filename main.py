from flask import Flask, request, jsonify, render_template
import os
import cv2
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Analyze blur and lighting with moderate sensitivity thresholds
def analyze_image(image_path):
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        # Return 4 values to match unpacking in endpoint
        return None, None, "Invalid image", "Invalid image"

    lap_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
    blur_status = (
        "Clear" if lap_var >= 100 else
        "Moderate" if lap_var >= 50 else
        "Blurry"
    )

    brightness = img_gray.mean()
    # Moderate lighting thresholds
    if brightness < 50:
        light_status = "Too Dark"
    elif brightness > 200:
        light_status = "Too Bright"
    else:
        light_status = "Good Lighting"

    return lap_var, brightness, blur_status, light_status

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/check-image-blur', methods=['POST'])
def check_image_blur():
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

if __name__ == '__main__':
    app.run(debug=True)
