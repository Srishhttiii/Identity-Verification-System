from deepface import DeepFace
import os


# Custom confidence threshold (%)
CONFIDENCE_THRESHOLD = 75.0


def verify_faces(id_file, selfie_file):
    id_path = "temp_id.jpg"
    selfie_path = "temp_selfie.jpg"


    try:
        id_file.save(id_path)
        selfie_file.save(selfie_path)


        print("Running DeepFace.verify...")


        result = DeepFace.verify(
            img1_path=id_path,
            img2_path=selfie_path,
            model_name="Facenet",
            detector_backend="mtcnn",
            enforce_detection=False
        )


        print("DeepFace result:", result)


        if "distance" not in result:
            return {"error": "Face not detected in one or both images."}


        distance = float(result["distance"])
        confidence = round((1 - distance) * 100, 2)
        is_match = confidence >= CONFIDENCE_THRESHOLD


        return {
            "match": is_match,
            "confidence_score": confidence,
            "distance": round(distance, 4)
        }


    except Exception as e:
        print("Face verification failed:", str(e))
        return {"error": str(e)}


    finally:
        if os.path.exists(id_path): os.remove(id_path)
        if os.path.exists(selfie_path): os.remove(selfie_path)


