import json
import os
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset...")

data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "LogisticRegression": LogisticRegression(max_iter=200),
    "DecisionTree": DecisionTreeClassifier()
}

results = {}

best_model = None
best_acc = 0

print("Training models...")

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"{name}: {acc:.4f}")

    results[name] = acc

    if acc > best_acc:
        best_acc = acc
        best_model = name
        joblib.dump(model, "best_model.pkl")

print("Saving experiment data...")

experiment = {
    "timestamp": datetime.now().isoformat(),
    "models": results,
    "best_model": best_model,
    "best_accuracy": best_acc
}

# Load existing history if exists
history_file = "experiment_log.json"

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
else:
    history = []

history.append(experiment)

with open(history_file, "w") as f:
    json.dump(history, f, indent=2)

print("Experiment logged.")

# 🧠 MODEL GATE (NEW IMPORTANT PART)
THRESHOLD = 0.90

if best_acc < THRESHOLD:
    raise Exception(f"Model rejected! Accuracy {best_acc:.2f} < {THRESHOLD}")

print("Model passed quality gate.")