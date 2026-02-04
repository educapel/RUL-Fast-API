import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
MODEL_PATH = "Models/lr_rul_pipeline.joblib"

INDEX_NAMES = ["unit_number", "time_cycles"]
SETTING_NAMES = ["setting_1", "setting_2", "setting_3"]


def load_model(model_path=MODEL_PATH):
    """Load the trained model."""
    model = joblib.load(model_path)
    print(f"Model loaded from: {model_path}")
    return model


def prepare_test_data(df_test: pd.DataFrame) -> pd.DataFrame:
    """
    Extract last cycle per unit for testing.
    Same logic as prepare_validation_data but for new test data.
    """
    return (
        df_test
        .groupby("unit_number")
        .last()
        .reset_index()
        .drop(columns=INDEX_NAMES + SETTING_NAMES)
    )


def prepare_single_input(sensor_dict: dict) -> pd.DataFrame:
    """
    Convert sensor dictionary to DataFrame for prediction.
    """
    return pd.DataFrame([sensor_dict])


def predict_rul(model, X):

    return model.predict(X)


def predict_single(model, sensor_dict):
    X = prepare_single_input(sensor_dict)
    return model.predict(X)[0]


def predict_batch(model, df_test):

    X_test = prepare_test_data(df_test)
    predictions = model.predict(X_test)

    results = pd.DataFrame({
        'unit_number': X_test.index + 1,
        'predicted_RUL': predictions
    })

    return results

def main():
    # Load model
    model = load_model()

    # Example 1: Single prediction
    print("\n--- Single Prediction ---")
    sensor_data = {f's_{i}': np.random.rand() * 100 for i in range(1, 22)}
    rul = predict_single(model, sensor_data)
    print(f"Predicted RUL: {rul:.2f} cycles")

    # Example 2: Batch prediction from file
    print("\n--- Batch Prediction ---")

    # Create sample test data
    sample_test = pd.DataFrame({
        'unit_number': np.repeat([1, 2, 3], 10),
        'time_cycles': np.tile(range(1, 11), 3),
        'setting_1': np.random.rand(30),
        'setting_2': np.random.rand(30),
        'setting_3': np.random.rand(30),
        **{f's_{i}': np.random.rand(30) * 100 for i in range(1, 22)}
    })

    results = predict_batch(model, sample_test)
    print(results)


if __name__ == "__main__":
    main()