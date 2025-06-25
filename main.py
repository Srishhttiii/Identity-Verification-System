from flask import Flask
from flask_cors import CORS
from ocr_module.routes import ocr_bp  # import your Blueprint

app = Flask(__name__)
CORS(app)

from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'frontend.html')

# Register the OCR route blueprint
app.register_blueprint(ocr_bp, url_prefix='/ocr')

if __name__ == '__main__':
    print(" Flask server running on http://localhost:5000")
    app.run(debug=True, port=5000)
