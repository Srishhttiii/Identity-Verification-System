from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from face_verification import verify_faces

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

@app.route("/")
def serve_frontend():
    return send_from_directory('.', 'frontend.html')

@app.route("/verify", methods=["POST"])
def verify():
    try:
        id_file = request.files.get("aadhar")
        selfie_file = request.files.get("selfie")

        if not id_file or not selfie_file:
            return jsonify({"error": "Missing file(s) in request"}), 400

        result = verify_faces(id_file, selfie_file)

        if "error" in result:
            return jsonify(result), 500

        return jsonify(result), 200

    except Exception as e:
        print("❌ Backend error:", e)  # For terminal debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
