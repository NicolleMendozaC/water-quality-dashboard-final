"""
train_model.py
Entrena un modelo Random Forest para clasificar la categoría del pH del agua
y guarda el modelo como model/model.pkl.
"""

import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

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
    "Water_Quality_testing.csv",
)

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


# ============================================================
# Variables del modelo
# ============================================================

FEATURES = [
    "Temperature (°C)",
    "Turbidity (NTU)",
    "Dissolved Oxygen (mg/L)",
    "Conductivity (µS/cm)",
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

    # División entrenamiento / prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # ========================================================
    # Balanceo de clases (SMOTE)
    # ========================================================

    smote = SMOTE(random_state=42)

    X_train, y_train = smote.fit_resample(
        X_train,
        y_train,
    )

    # ========================================================
    # Modelo
    # ========================================================

    pipeline = Pipeline([
        (
            "clf",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42,
            ),
        )
    ])

    # Entrenamiento
    pipeline.fit(X_train, y_train)

    # ========================================================
    # Validación Cruzada
    # ========================================================

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    cv_scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring="f1_weighted",
    )

    # ========================================================
    # Predicciones
    # ========================================================

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # ========================================================
    # Métricas
    # ========================================================

    metrics = {

        "accuracy": round(
            accuracy_score(y_test, y_pred),
            4,
        ),

        "precision": round(
            precision_score(y_test, y_pred),
            4,
        ),

        "recall": round(
            recall_score(y_test, y_pred),
            4,
        ),

        "f1": round(
            f1_score(y_test, y_pred),
            4,
        ),

        "roc_auc": round(
            roc_auc_score(y_test, y_proba),
            4,
        ),

        "cv_f1_mean": round(
            cv_scores.mean(),
            4,
        ),

        "cv_f1_std": round(
            cv_scores.std(),
            4,
        ),

        "confusion_matrix": confusion_matrix(
            y_test,
            y_pred,
        ).tolist(),

        "y_test": y_test.tolist(),

        "y_proba": y_proba.tolist(),

        "features": FEATURES,

        "target": TARGET,
    }

    # ========================================================
    # Guardar modelo
    # ========================================================

    joblib.dump(
        {
            "pipeline": pipeline,
            "metrics": metrics,
        },
        MODEL_PATH,
    )

    # ========================================================
    # Resultados
    # ========================================================

    print("\n===================================")
    print("Modelo entrenado correctamente")
    print("===================================")

    print(f"Accuracy : {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall   : {metrics['recall']}")
    print(f"F1 Score : {metrics['f1']}")
    print(f"ROC AUC  : {metrics['roc_auc']}")

    print("\n===== Validación Cruzada =====")
    print(f"F1 promedio : {metrics['cv_f1_mean']}")
    print(f"Desviación  : {metrics['cv_f1_std']}")

    print(f"\nModelo guardado en:\n{MODEL_PATH}")

    return metrics


# ============================================================
# Ejecutar
# ============================================================

if __name__ == "__main__":
    train_and_save()