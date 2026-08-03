import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ----------------------------
# Load Processed Dataset
# ----------------------------

df = pd.read_csv("dataset/processed_train.csv")

print("Processed Dataset Loaded Successfully")

# ----------------------------
# Features & Target
# ----------------------------

X = df.drop(columns=["label"])
y = df["label"]

# ----------------------------
# Split Dataset
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(f"Training Samples : {X_train.shape[0]}")
print(f"Testing Samples  : {X_test.shape[0]}")

# ----------------------------
# Train Model
# ----------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nModel Training Completed!")

# ----------------------------
# Predictions
# ----------------------------

predictions = model.predict(X_test)

# ----------------------------
# Evaluation
# ----------------------------

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# ----------------------------
# Save Model
# ----------------------------

joblib.dump(model, "models/model.pkl")

print("\nModel Saved Successfully!")