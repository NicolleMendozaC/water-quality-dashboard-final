"""
train_model.py
Entrena una Regresión Logística para clasificar la calidad del pH del agua
y guarda el modelo como model/model.pkl.
"""

import sys
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix,
                             roc_auc_score)
from sklearn.pipeline import Pipeline

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "synthetic_water_quality.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# ── Características usadas en el modelo ──────────────────────────────────────
FEATURES = ["ph", "temperature_c", "turbidity_ntu",
            "dissolved_oxygen", "conductivity_us"]
TARGET   = "ph_category"


def load_or_generate_data() -> pd.DataFrame:
    """Carga el CSV sintético; si no existe, lo genera primero."""
    if not os.path.exists(DATA_PATH):
        print("CSV sintético no encontrado. Generando datos…")
        sys.path.insert(0, os.path.join(BASE_DIR, "..", "data"))
        from generate_data import generate_water_quality_data
        df = generate_water_quality_data()
        df.to_csv(DATA_PATH, index=False)
        print(f"Datos guardados en {DATA_PATH}")
    else:
        df = pd.read_csv(DATA_PATH)
    return df


def train_and_save() -> dict:
    """
    Entrena el modelo y guarda model.pkl.

    Retorna un diccionario con las métricas del conjunto de prueba.
    """
    df = load_or_generate_data()

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # Pipeline: escalar + regresión logística
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf",    LogisticRegression(max_iter=500, random_state=42)),
    ])

    pipeline.fit(X_train, y_train)

    # ── Métricas ──────────────────────────────────────────────────────────────
    y_pred  = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy"        : round(accuracy_score(y_test, y_pred),  4),
        "precision"       : round(precision_score(y_test, y_pred), 4),
        "recall"          : round(recall_score(y_test, y_pred),    4),
        "f1"              : round(f1_score(y_test, y_pred),        4),
        "roc_auc"         : round(roc_auc_score(y_test, y_proba),  4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "y_test"          : y_test.tolist(),
        "y_proba"         : y_proba.tolist(),
        "features"        : FEATURES,
        "target"          : TARGET,
    }

    # ── Guardar modelo ────────────────────────────────────────────────────────
    joblib.dump({"pipeline": pipeline, "metrics": metrics}, MODEL_PATH)
    print(f"\nModelo guardado en {MODEL_PATH}")
    print(f"  Accuracy : {metrics['accuracy']}")
    print(f"  Precision: {metrics['precision']}")
    print(f"  Recall   : {metrics['recall']}")
    print(f"  F1-Score : {metrics['f1']}")
    print(f"  ROC-AUC  : {metrics['roc_auc']}")

    return metrics


if __name__ == "__main__":
    train_and_save()
