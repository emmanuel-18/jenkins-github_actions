print("Hello from GitHub Jenkins integration")

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
import joblib
import numpy as np
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()


history_file = os.getenv("history_file")

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
else:    history = []

app = FastAPI()

model = joblib.load("best_model.pkl")

class InputData(BaseModel):
    features: List[float]

class_names = ["setosa", "versicolor", "virginica"]
    

@app.get("/")
def home():
    return {"message": "ML Model API is running"}

@app.post("/predict")
def predict(input_data: InputData):
    data = np.array(input_data.features).reshape(1, -1)

    proba = model.predict_proba(data)[0]

    pred_index = np.argmax(proba)
    confidence = proba[pred_index]

    prediction = class_names[pred_index]
    confidence = proba[pred_index]

    # logs
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": request.features,
        "prediction": prediction,
        "confidence": confidence
    }

    history.append(entry)

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    return {
        "prediction": prediction,
        "confidence": confidence
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
        }

@app.get("/version")
def version():
    return {
        "version": "1.0.0",
        "framework": "sklearn",
        "api": "v1"
        }

@app.get("/history")
def get_history():  
    return {
        "total_predictions": len(history),
        "data": history
    }
