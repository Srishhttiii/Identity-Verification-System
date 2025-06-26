import cv2


def analyze_image(image_path):
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        return None, None, "Invalid image", "Invalid image"


    lap_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
    blur_status = (
        "Clear" if lap_var >= 100 else
        "Moderate" if lap_var >= 50 else
        "Blurry"
    )


    brightness = img_gray.mean()
    light_status = (
        "Too Dark" if brightness < 50 else
        "Too Bright" if brightness > 200 else
        "Good Lighting"
    )


    return lap_var, brightness, blur_status, light_status


