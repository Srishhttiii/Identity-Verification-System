import cv2
import numpy as np
img = cv2.imread("cool copy.jpeg" , cv2.IMREAD_GRAYSCALE)

laplacian_var = cv2.Laplacian(img , cv2.CV_64F).var()
print(laplacian_var)

if laplacian_var < 50 :
    print("image is blurry ...go chnge it idiot ")
# cv2.imshow("laplacian" , laplacian)
# cv2.imshow("asse hi" , img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()












# from flask import Flask, request, jsonify, send_from_directory, render_template_string
# import cv2
# import numpy as np
# import os
#
# app = Flask(__name__)
#
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <title>Blur Detector</title>
# </head>
# <body>
#   <h2>Upload Image to Check Blurriness</h2>
#   <form id="uploadForm" enctype="multipart/form-data">
#     <input type="file" name="image" accept="image/*" required>
#     <button type="submit">Check Blur</button>
#   </form>
#   <p id="result"></p>
#
#   <script>
#     document.getElementById('uploadForm').onsubmit = async function(e) {
#       e.preventDefault();
#       const formData = new FormData(this);
#
#       try {
#         const response = await fetch('/check_blur', {
#           method: 'POST',
#           body: formData
#         });
#
#         const data = await response.json();
#         document.getElementById('result').textContent = data.message || data.error;
#       } catch (error) {
#         document.getElementById('result').textContent = "Error: " + error.message;
#       }
#     };
#   </script>
# </body>
# </html>
# """
#
# @app.route('/')
# def serve_frontend():
#     return render_template_string(HTML_TEMPLATE)
#
# def detect_blur(image_path):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         return None
#     laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
#     return laplacian_var
#
# @app.route('/check_blur', methods=['POST'])
# def check_blur():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
#
#     image_file = request.files['image']
#     if image_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#
#     os.makedirs("uploads", exist_ok=True)
#     image_path = os.path.join("uploads", image_file.filename)
#     image_file.save(image_path)
#
#     lap_var = detect_blur(image_path)
#     os.remove(image_path)
#
#     if lap_var is None:
#         return jsonify({'error': 'Invalid image'}), 400
#
#     lap_var = float(lap_var)
#     is_blur = bool(lap_var < 50)
#
#     result = {
#         "laplacian_variance": lap_var,
#         "is_blurry": is_blur,
#         "message": "Image is blurry. Please upload a clearer one." if is_blur else "Image is clear."
#     }
#
#     return jsonify(result)
#
# if __name__ == '__main__':
#     app.run(debug=True)
