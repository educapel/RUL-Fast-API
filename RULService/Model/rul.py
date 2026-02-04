import joblib
import pandas as pd


MODEL_PATH = "Models/lr_rul_pipeline.joblib"
SENSOR_NAMES = [f"s_{i+1}" for i in range(21)]


def load_model(model_path=MODEL_PATH):
    """Load the trained model."""
    model = joblib.load(model_path)
    print(f"Model loaded from: {model_path}")
    return model


class RULPredictor:
    def __init__(self, model_path: str = MODEL_PATH):

        self.model = self._load_model(model_path)
        self.feature_names = SENSOR_NAMES

    def _load_model(self, model_path: str):
        """Load the trained model from disk."""
        try:
            model = joblib.load(model_path)
            print(f"✓ Model loaded successfully from: {model_path}")
            return model
        except FileNotFoundError:
            raise FileNotFoundError(f"Model not found at: {model_path}")
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")

    def predict(self, sensor_dict: dict) -> float:
        sensor_pd = pd.DataFrame([sensor_dict])

        return self.model.predict(sensor_pd)[0]


