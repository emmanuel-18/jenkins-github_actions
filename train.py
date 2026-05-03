import json
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

best_model_name = None
best_accuracy = 0

print("Training models...")

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"{name} accuracy: {acc:.4f}")

    results[name] = acc

    if acc > best_accuracy:
        best_accuracy = acc
        best_model_name = name
        joblib.dump(model, "best_model.pkl")

print("Saving results...")

output = {
    "models": results,
    "best_model": best_model_name,
    "best_accuracy": best_accuracy
}

with open("experiment_results.json", "w") as f:
    json.dump(output, f)

print("Done.")