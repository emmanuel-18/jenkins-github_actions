import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

print("Step 1: Loading dataset")

data = load_iris()
X = data.data
y = data.target

print("Step 2: Splitting data")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Step 3: Training model")

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

print("Step 4: Evaluating model")

accuracy = model.score(X_test, y_test)

print(f"Accuracy = {accuracy:.2f}")

print("Step 5: Saving model and metrics")

# Save model
joblib.dump(model, "model.pkl")

# Save metrics
metrics = {
    "model": "LogisticRegression",
    "accuracy": accuracy
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f)

print("Done")