# main.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from ocr_module.routes import ocr_bp
from blur_module.routes import blur_bp
from face_module.routes import face_bp






app = Flask(__name__)
CORS(app)


@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'frontend.html')


# Register Blueprints
app.register_blueprint(ocr_bp, url_prefix='/ocr')
print("✅ ocr_bp blueprint registered!")


app.register_blueprint(face_bp, url_prefix='/face')
print("✅ face_bp blueprint registered!")


app.register_blueprint(blur_bp, url_prefix='/blur')
print("✅ blur_bp blueprint registered!")




if __name__ == '__main__':
    print("✅ Flask server running on http://localhost:5000")
    app.run(debug=True, port=5000)



