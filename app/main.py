from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Darija Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des modèles
vec   = joblib.load("models/darija_vectorizer.pkl")
model = joblib.load("models/darija_model.pkl")
le    = joblib.load("models/darija_label_encoder.pkl")

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "running", "classes": list(le.classes_)}

@app.post("/predict")
def predict(input: TextInput):
    X          = vec.transform([input.text])
    pred_idx   = model.predict(X)[0]
    pred_label = le.classes_[pred_idx]
    proba      = model.predict_proba(X)[0]
    confidence = round(float(proba.max()), 3)

    top3_idx = np.argsort(proba)[-3:][::-1]
    top3 = [
        {"label": le.classes_[i], "score": round(float(proba[i]), 3)}
        for i in top3_idx
    ]

    return {
        "prediction": pred_label,
        "confidence": confidence,
        "top3"      : top3
    }