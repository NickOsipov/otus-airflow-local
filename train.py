"""
Module: train.py
Description: This module is used to train a machine learning model.
"""

import os

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def load_data(data_path: str):
    """
    Load data from a CSV file.
    """
    return pd.read_csv(data_path, sep=";")

def prepare_data(data: pd.DataFrame, target: str="quality"):
    """
    Prepare data for training.
    """
    X = data.drop(target, axis=1)
    y = data[target]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """
    Train a machine learning model.
    """
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate a machine learning model.
    """
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return mae

def save_model(model, model_path: str):
    """
    Save a machine learning model.
    """
    joblib.dump(model, model_path)


def main():
    """
    Main function.
    """
    data = load_data(os.path.join("data", "winequality-red.csv"))
    X_train, X_test, y_train, y_test = prepare_data(data)
    model = train_model(X_train, y_train)
    mae = evaluate_model(model, X_test, y_test)
    print(f"MAE: {mae}")
    save_model(model, os.path.join("models", "model.joblib"))

if __name__ == "__main__":
    main()
