import os
import cv2
import numpy as np
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "leaf_disease_svm.pkl")

model = joblib.load(MODEL_PATH)

IMG_SIZE = 128

def extract_features(image):
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [32], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [32], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [32], [0, 256])

    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()

    return np.concatenate([hist_h, hist_s, hist_v])


@api_view(['POST'])
def predict(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    img_file = request.FILES['image']
    img_array = np.frombuffer(img_file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image is None:
        return Response({"error": "Invalid image"}, status=400)

    features = extract_features(image).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = float(np.max(model.predict_proba(features)))

    return Response({
        "disease": prediction,
        "confidence": round(confidence, 2)
    })
