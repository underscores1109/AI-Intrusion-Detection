"""
Utility Functions
Reusable functions used throughout the project.
"""

import joblib
import pandas as pd


def load_csv(path):
    """
    Load a CSV or TXT dataset.
    """
    return pd.read_csv(path)


def save_csv(dataframe, path):
    """
    Save dataframe to CSV.
    """
    dataframe.to_csv(path, index=False)


def save_model(model, path):
    """
    Save ML model.
    """
    joblib.dump(model, path)


def load_model(path):
    """
    Load ML model.
    """
    return joblib.load(path)