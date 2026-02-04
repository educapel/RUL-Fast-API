#!/usr/bin/env python
# coding: utf-8

# In[115]:


import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import pickle
import os
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
import warnings
import joblib

warnings.filterwarnings('ignore')


INDEX_NAMES = ["unit_number", "time_cycles"]
SETTING_NAMES = ["setting_1", "setting_2", "setting_3"]
SENSOR_NAMES = [f"s_{i+1}" for i in range(21)]
COL_NAMES = INDEX_NAMES + SETTING_NAMES + SENSOR_NAMES



def load_cmapss_data(base_path: Path):
    """
    Load CMAPSS FD001 train, test, and RUL files.
    """
    data_dir = base_path / "CMAPSSData"

    df_train = pd.read_csv(
        data_dir / "train_FD001.txt",
        sep=r"\s+",
        header=None,
        names=COL_NAMES
    )

    df_valid = pd.read_csv(
        data_dir / "test_FD001.txt",
        sep=r"\s+",
        header=None,
        names=COL_NAMES
    )

    y_valid = pd.read_csv(
        data_dir / "RUL_FD001.txt",
        sep=r"\s+",
        header=None,
        names=["RUL"]
    )

    return df_train, df_valid, y_valid


def add_rul_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Remaining Useful Life (RUL) per unit.
    """
    max_cycles = df.groupby("unit_number")["time_cycles"].max()

    df = df.merge(
        max_cycles.rename("max_time_cycle"),
        left_on="unit_number",
        right_index=True
    )

    df["RUL"] = df["max_time_cycle"] - df["time_cycles"]

    return df.drop(columns="max_time_cycle")

# In[123]:


def prepare_train_test_data(
    df: pd.DataFrame,
    test_size: float = 0.3,
    random_state: int = 42
):
    """
    Prepare X/y and split into train/test.
    """
    drop_cols = INDEX_NAMES + SETTING_NAMES

    X = df.drop(columns=drop_cols)
    y = X["RUL"]

    X = X.drop(columns="RUL")

    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state
    )

def prepare_validation_data(df_valid: pd.DataFrame) -> pd.DataFrame:
    """
    Extract last cycle per unit for validation.
    """
    return (
        df_valid
        .groupby("unit_number")
        .last()
        .reset_index()
        .drop(columns=INDEX_NAMES + SETTING_NAMES)
    )

def scale_features(X_train, X_test, X_valid):
    """
    Fit scaler on training data only and transform all sets.
    """
    scaler = MinMaxScaler()

    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    X_valid_s = scaler.transform(X_valid)

    return X_train_s, X_test_s, X_valid_s, scaler


def get_sensor_dictionary():
    """
    Human-readable sensor descriptions.
    """
    descriptions = [
        "(Fan inlet temperature) (◦R)",
        "(LPC outlet temperature) (◦R)",
        "(HPC outlet temperature) (◦R)",
        "(LPT outlet temperature) (◦R)",
        "(Fan inlet Pressure) (psia)",
        "(bypass-duct pressure) (psia)",
        "(HPC outlet pressure) (psia)",
        "(Physical fan speed) (rpm)",
        "(Physical core speed) (rpm)",
        "(Engine pressure ratio (P50/P2))",
        "(HPC outlet static pressure) (psia)",
        "(Ratio of fuel flow to Ps30) (pps/psia)",
        "(Corrected fan speed) (rpm)",
        "(Corrected core speed) (rpm)",
        "(Bypass Ratio)",
        "(Burner fuel-air ratio)",
        "(Bleed Enthalpy)",
        "(Required fan speed)",
        "(Required fan conversion speed)",
        "(High-pressure turbine cool air flow)",
        "(Low-pressure turbine cool air flow)",
    ]

    return {f"s_{i+1}": desc for i, desc in enumerate(descriptions)}


def evaluate(y_true, y_hat, label='test'):
    mse = mean_squared_error(y_true, y_hat)
    rmse = np.sqrt(mse)
    variance = r2_score(y_true, y_hat)
    print('{} set RMSE:{}, R2:{}'.format(label, rmse, variance))


def train_model(X_train, y_train, X_test, y_test, X_valid, y_valid):
    """Train Linear Regression model and evaluate on all datasets."""

    print("\n🤖 Training Linear Regression model...")

    # Create pipeline: scaling + model
    model = Pipeline([
        ('scaler', MinMaxScaler()),
        ('regression', LinearRegression())
    ])

    # Train
    model.fit(X_train, y_train)
    print("   ✓ Training complete!")

    # Evaluate on all datasets
    all_metrics = {}

    # Training set
    y_train_pred = model.predict(X_train)
    all_metrics['train'] = evaluate(y_train, y_train_pred, "Train")

    # Test set
    y_test_pred = model.predict(X_test)
    all_metrics['test'] = evaluate(y_test, y_test_pred, "Test")

    # Validation set
    y_valid_pred = model.predict(X_valid)
    all_metrics['validation'] = evaluate(y_valid, y_valid_pred, "Validation")

    return model, all_metrics


def save_model(model, base_dir):

    models_folder = base_dir / "Models"

    # Save model with simple name
    model_path = models_folder / "lr_rul_pipeline.joblib"
    joblib.dump(model, model_path)

    print(f"   ✓ Model saved: {model_path}")



def main():
    # Resolve project root (RUL-Fast-API/)
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load data
    df_train, df_valid, y_valid = load_cmapss_data(BASE_DIR)

    # Feature engineering
    df_train = add_rul_column(df_train)

    # Train/test split
    X_train, X_test, y_train, y_test = prepare_train_test_data(df_train)

    # Validation features
    X_valid = prepare_validation_data(df_valid)

    # Scaling
    X_train_s, X_test_s, X_valid_s, scaler = scale_features(
        X_train, X_test, X_valid
    )


    # Get feature names
    feature_names = list(X_train.columns)

    # Step 4: Train model
    model, metrics = train_model(
        X_train, y_train,
        X_test, y_test,
        X_valid, y_valid
    )

    # Step 5: Save model
    save_model(model, BASE_DIR)



if __name__ == "__main__":
    main()
