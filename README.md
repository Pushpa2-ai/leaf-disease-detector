🌿 Plant Leaf Disease Detection System
## 🎥 Demo

![Plant Leaf Disease Detection Demo](frontend/src/assets/detection-demo.gif)


Plant Leaf Disease Detection is a cloud-deployed, ML-powered decision-support system designed to perform real-time plant disease inference with confidence-based risk assessment, severity classification, and automated action recommendations. The platform is built with a production-grade full-stack architecture featuring a decoupled frontend, REST-based inference workflow, and scalable backend deployment.


🌟 Key Features

✅ 1. Image-Based Leaf Disease Detection

Upload plant leaf images (JPG, JPEG, PNG)

Real-time disease prediction using a classical ML model

Automatic image preprocessing before inference

Supports known disease classes with out-of-scope detection

✅ 2. ML-Powered Prediction & Safety Engine

Classical Machine Learning–based image classification (HSV feature extraction + SVM)

Trained on a curated subset of the PlantVillage dataset

Returns:

Predicted disease name

Confidence score

Unknown detection for low-confidence or unsupported inputs

Example Output:

Disease: Early Blight

Confidence: 0.84

Severity: Medium

Recommendation: Monitor for 48 hours

✅ 3. Modern, Interactive Dashboard

Clean, green-themed UI

Drag-and-drop image upload

Controlled image preview (no layout shift)

Dynamic layout (centered upload → two-column view after result)

Smooth slide-in information panel

✅ 4. Disease Knowledge Base & Decision Support

Backend-driven knowledge base for:

Symptoms

Prevention and treatment guidance

Severity engine (Low / Medium / High risk)

Rule-based action recommendations:

Immediate action recommended

Monitor for 48 hours

No action needed

✅ 5. Full-Stack ML Integration

End-to-end flow:

Frontend → REST API → ML Inference → Knowledge Base → Decision Engine → Frontend

Modular backend design for easy extension to new crops and diseases

Deployment-ready architecture


🏗️ System Architecture

Deployed on cloud infrastructure with environment-based configuration and CORS-secured API access
```text

Frontend (React + Vite + Tailwind CSS) — Vercel
        |
        |  HTTPS REST API (Image Upload + JSON Response)
        |
Backend (Django + Django REST Framework) — Render
        |
ML Inference (HSV Feature Extraction + SVM)
        |
Knowledge Base + Severity & Recommendation Engine

```


🏗️ Tech Stack


🎨 Frontend

React.js (Vite)

Tailwind CSS

JavaScript (ES6+)


🧠 Backend

Django

Django REST Framework

Python


🤖 Machine Learning

Scikit-learn

OpenCV

NumPy

Classical ML algorithms (no deep learning)


⚙️ DevOps & Deployment

GitHub (Version Control)

Render (Backend Hosting)

Vercel (Frontend Hosting)

Environment-Based API Routing


📂 Project Structure
```text
leaf-disease-detector/
│
├── README.md
├── .gitignore
├── requirements.txt              
│
├── ml/                           
│   ├── dataset/
│   │   ├── Corn___Common_Rust/
│   │   ├── Potato___Early_blight/
│   │   ├── Potato___Healthy/
│   │   ├── Tomato___Early_blight/
│   │   └── Tomato___Healthy/
│   │
│   ├── models/
│   │   └── leaf_disease_svm.pkl
│   │
│   └── scripts/                  
│       └── train_model.py     
│
├── backend/
│   ├── manage.py
│   │
│   ├── backend/                  
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── api/                      
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── views.py              
│   │   ├── knowledge_base.py
│   │   └── migrations/
│   │       └── __init__.py
│   │
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   │
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│   │   │
│   │   ├── components/
│   │   │   └── Dashboard.jsx
│   │   │
│   │   └── assets/
│   │       ├── bg.png
│   │       └── demo.gif
│   │
│   └── .env.example
│
```


⚙️ Environment Setup

.env

Create a .env file in backend:

SECRET_KEY=your_secret

DEBUG=False


🛠 Backend

cd backend

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver


🎨 Frontend

cd frontend

npm install

npm run dev


🌐 Deployment (Production Ready)

Backend

Hosted on Render: https://leaf-disease-detector-6p6p.onrender.com

Gunicorn + Whitenoise

Frontend

Hosted on Vercel: https://leaf-disease-detector-three.vercel.app/

Environment-based API routing:

VITE_API_BASE=https://leaf-disease-detector-6p6p.onrender.com


⚙️ Other Tools

Postman (API testing)

Git & GitHub

NPM

Python Virtual Environment


📥 How to Clone & Run the Project


🖥️ 1. Clone the Repository

git clone https://github.com/Pushpa2-ai/leaf-disease-detector.git

cd leaf-disease-detector

🛠️ Backend Setup

cd backend

python -m venv venv

venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

Backend will run on:

👉 http://127.0.0.1:8000


🎨 Frontend Setup

cd frontend

npm install

npm run dev

Frontend will run on:

👉 http://localhost:5173


🧠 ML Logic Inside Plant Leaf Disease Detection

Feature	ML / Logic Used

Image preprocessing	OpenCV (resize, normalization)

Feature extraction	Texture, color, shape features

Classification	Classical ML (Scikit-learn)

Confidence scoring	Probability-based output

Prediction pipeline	REST API integration

Dataset: PlantVillage (processed & filtered)

Model: Classical ML classifier using extracted image features


🚀 Future Enhancements


🌱 Support for more plant species & diseases

🧠 Deep Learning model integration (CNN)

📱 Mobile-responsive UI improvements

📊 Admin analytics dashboard

📸 Camera-based live detection


📄 License

MIT License — Free to use and improve.


🤝 Contributing

Feel free to fork this repository, submit pull requests, or open issues for improvements.

🙌 Author

Pushpa Kumari

👩‍💻 B.Tech (CSE-AIDS) | Full-Stack Developer (React & Django)

🔥 Focused on building cloud-deployed, API-driven applications with real-world simulation and production-style architecture.
