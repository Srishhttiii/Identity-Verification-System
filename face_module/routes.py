from flask import Blueprint, request, jsonify
from face_module.face_verification import verify_faces


face_bp = Blueprint('face', __name__)


@face_bp.route("/verify", methods=["POST"])
def verify():
    print("📸 /face/verify endpoint hit!")
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
        print("❌ Backend error:", e)
        return jsonify({"error": str(e)}), 500