"""
train_model.py
Entrena una Regresión Logística para clasificar la calidad del pH del agua
y guarda el modelo como model/model.pkl.
"""

import os
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
)

# ============================================================
# Rutas
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "Water_Quality_testing.csv"
)

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


# ============================================================
# Variables del modelo
# ============================================================

FEATURES = [
    "Temperature (°C)",
    "Turbidity (NTU)",
    "Dissolved Oxygen (mg/L)",
    "Conductivity (µS/cm)"
]



TARGET = "ph_category"


# ============================================================
# Cargar datos
# ============================================================

def load_data():

    df = pd.read_csv(DATA_PATH)

    # Crear variable objetivo
    df["ph_category"] = (df["pH"] >= 7.0).astype(int)

    return df


# ============================================================
# Entrenar modelo
# ============================================================

def train_and_save():

    df = load_data()

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=500, random_state=42)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {

        "accuracy": round(
            accuracy_score(y_test, y_pred), 4
        ),

        "precision": round(
            precision_score(y_test, y_pred), 4
        ),

        "recall": round(
            recall_score(y_test, y_pred), 4
        ),

        "f1": round(
            f1_score(y_test, y_pred), 4
        ),

        "roc_auc": round(
            roc_auc_score(y_test, y_proba), 4
        ),

        "confusion_matrix": confusion_matrix(
            y_test,
            y_pred
        ).tolist(),

        "y_test": y_test.tolist(),

        "y_proba": y_proba.tolist(),

        "features": FEATURES,

        "target": TARGET,
    }

    joblib.dump(
        {
            "pipeline": pipeline,
            "metrics": metrics,
        },
        MODEL_PATH,
    )

    print("\n===================================")
    print("Modelo entrenado correctamente")
    print("===================================")

    print(f"Accuracy : {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall   : {metrics['recall']}")
    print(f"F1 Score : {metrics['f1']}")
    print(f"ROC AUC  : {metrics['roc_auc']}")

    print(f"\nModelo guardado en:\n{MODEL_PATH}")

    return metrics


# ============================================================
# Ejecutar
# ============================================================

if __name__ == "__main__":
    train_and_save()
