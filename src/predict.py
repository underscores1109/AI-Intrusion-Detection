import pandas as pd
import joblib
import os
from datetime import datetime

from src.config import MODEL_PATH, PREDICTION_OUTPUT


class IntrusionDetector:

    def __init__(self):
        print("=" * 60)
        print("Loading Trained AI Model...")
        print("=" * 60)

        self.model = joblib.load(MODEL_PATH)

        print("Model Loaded Successfully!\n")

    def predict_dataset(self, csv_path):

        print("Loading Dataset...")

        df = pd.read_csv(csv_path)

        # Remove label column if available
        if "label" in df.columns:
            X = df.drop(columns=["label"])
        else:
            X = df.copy()

        print("Running AI Prediction...")

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        prediction_labels = []
        confidence_scores = []
        status_list = []

        for prediction, probability in zip(predictions, probabilities):

            if prediction == 0:
                label = "Attack"
                status = "ALERT"
            else:
                label = "Normal"
                status = "OK"

            prediction_labels.append(label)
            status_list.append(status)

            confidence_scores.append(
                round(max(probability) * 100, 2)
            )

        # Add prediction columns
        df["Prediction"] = prediction_labels
        df["Confidence (%)"] = confidence_scores

        # Save prediction CSV
        os.makedirs("outputs", exist_ok=True)
        df.to_csv(PREDICTION_OUTPUT, index=False)

        # Generate Splunk Logs
        os.makedirs("logs", exist_ok=True)

        log_df = pd.DataFrame({

            "Timestamp": [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for _ in range(len(df))
            ],

            "Prediction": prediction_labels,

            "Confidence": confidence_scores,

            "Status": status_list

        })

        log_df.to_csv(
            "logs/intrusion_logs.csv",
            index=False
        )

        print("\nPredictions Saved Successfully!")
        print("Security Logs Generated Successfully!")

        print("\nPrediction Summary")
        print("-" * 40)
        print(f"Total Records : {len(df)}")
        print(f"Attack        : {prediction_labels.count('Attack')}")
        print(f"Normal        : {prediction_labels.count('Normal')}")
        print("-" * 40)

        return df


if __name__ == "__main__":

    detector = IntrusionDetector()

    detector.predict_dataset(
        "dataset/processed_test.csv"
    )