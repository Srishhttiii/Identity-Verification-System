from deepface import DeepFace
import os


# Custom confidence threshold
CONFIDENCE_THRESHOLD = 75.0


def verify_faces(id_file, selfie_file):
    id_path = "temp_id.jpg"
    selfie_path = "temp_selfie.jpg"


    try:
        # Save uploaded files temporarily
        id_file.save(id_path)
        selfie_file.save(selfie_path)


        # Perform face verification
        result = DeepFace.verify(
            img1_path=id_path,
            img2_path=selfie_path,
            model_name="Facenet",
            detector_backend="mtcnn",
            enforce_detection=False
        )


        # Calculate custom confidence score
        distance = float(result["distance"])
        confidence = round((1 - distance) * 100, 2)
        is_match = confidence >= CONFIDENCE_THRESHOLD


        return {
            "match": is_match,
            "confidence_score": confidence,
            "distance": round(distance, 4)
        }


    except Exception as e:
        return {"error": str(e)}


    finally:
        # Cleanup temporary files
        if os.path.exists(id_path):
            os.remove(id_path)
        if os.path.exists(selfie_path):
            os.remove(selfie_path)


