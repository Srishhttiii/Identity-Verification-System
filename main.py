# flask code 
from flask import Flask #to create web application
from flask_cors import CORS # CORS(Cross-Origin Resource Sharing)
from ocr_module.routes import ocr_bp  # import your Blueprint

app = Flask(__name__)   #instance of flask application
CORS(app)

from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'frontend.html')

# Register the imported blueprint 'ocr_bp' under the '/ocr' URL prefix
# All the routes defined inside the ocr_bp blueprint will be accessible via URLs starting with '/ocr'
app.register_blueprint(ocr_bp, url_prefix='/ocr')

if __name__ == '__main__':
    print(" Flask server running on http://localhost:5000")
    app.run(debug=True, port=5000)
