import os
import cv2
import numpy as np
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .knowledge_base import DISEASE_KNOWLEDGE
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "ml" / "models" / "leaf_disease_svm.pkl"

_model = None

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model


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

def get_severity(disease, confidence):
    if disease == "Healthy":
        return "Low"

    if confidence > 0.85:
        return "High"
    elif confidence > 0.7:
        return "Medium"
    else:
        return "Low"

def get_recommendation(severity):
    if severity == "High":
        return "Immediate action recommended"
    elif severity == "Medium":
        return "Monitor for 48 hours"
    else:
        return "No action needed"


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
    model = get_model()
    prediction = model.predict(features)[0]
    probs = model.predict_proba(features)
    confidence = float(np.max(probs))


    # Split label
    parts = prediction.split("___")
    disease = parts[1].replace("_", " ").title() if len(parts) > 1 else prediction

    # Get knowledge
    info = DISEASE_KNOWLEDGE.get(disease, {})

    THRESHOLD = 0.6

    if confidence < THRESHOLD:
        return Response({
            "disease": "Unknown",
            "confidence": round(confidence, 2),
            "message": "This image does not match known disease classes"
        })

    severity = get_severity(disease, confidence)
    recommendation = get_recommendation(severity)

    return Response({
        "disease": disease,
        "confidence": round(confidence, 2),
        "severity": severity,
        "recommendation": recommendation,
        "symptoms": info.get("symptoms", []),
        "prevention": info.get("prevention", [])
    })
