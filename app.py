print("Hello from GitHub Jenkins integration")

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
import joblib
import numpy as np
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

model = joblib.load("best_model.pkl")

class InputData(BaseModel):
    features: List[float]

class_names = ["setosa", "versicolor", "virginica"]

history_file = os.getenv("history_file", "prediction_history.json")

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
else:
    history = []


@app.get("/")
def home():
    return {"message": "ML Model API is running"}


@app.post("/predict")
def predict(input_data: InputData):
    data = np.array(input_data.features).reshape(1, -1)

    proba = model.predict_proba(data)[0]

    pred_index = int(np.argmax(proba))
    prediction = class_names[pred_index]
    confidence = float(proba[pred_index])

    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_data.features,
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