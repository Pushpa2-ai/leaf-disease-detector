import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")

IMG_SIZE = 128


def extract_features(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hist_h = cv2.calcHist([hsv], [0], None, [32], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [32], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [32], [0, 256])

    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()

    return np.concatenate([hist_h, hist_s, hist_v])


def load_data():
    X, y = [], []

    for label in os.listdir(DATASET_DIR):
        class_path = os.path.join(DATASET_DIR, label)
        if not os.path.isdir(class_path):
            continue

        print(f"Loading {label}...")

        for file in os.listdir(class_path):
            if file.lower().endswith((".jpg", ".png", ".jpeg")):
                img_path = os.path.join(class_path, file)
                features = extract_features(img_path)
                if features is not None:
                    X.append(features)
                    y.append(label)

    return np.array(X), np.array(y)


def main():
    print("Loading dataset...")
    X, y = load_data()
    print("Total samples:", len(y))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training SVM model...")
    model = SVC(kernel="rbf", probability=True)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "leaf_disease_svm.pkl"))
    print("Model saved successfully!")


if __name__ == "__main__":
    main()
