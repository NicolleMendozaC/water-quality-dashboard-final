"""
generate_data.py
Genera datos sintéticos de calidad del agua para entrenamiento del modelo.
La variable objetivo es 'ph_category': 0 = Ácido (pH < 7), 1 = Neutro/Alcalino (pH >= 7)
"""

import numpy as np
import pandas as pd

def generate_water_quality_data(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    Genera un DataFrame sintético de calidad del agua.

    Parámetros
    ----------
    n_samples : int
        Número de muestras a generar.
    random_state : int
        Semilla para reproducibilidad.

    Retorna
    -------
    pd.DataFrame con variables fisicoquímicas y la columna objetivo 'ph_category'.
    """
    rng = np.random.default_rng(random_state)

    ph              = rng.uniform(6.5, 8.5, n_samples).round(2)
    temperature     = rng.uniform(15.0, 35.0, n_samples).round(2)
    turbidity       = rng.uniform(0.5, 10.0, n_samples).round(2)
    dissolved_oxygen= rng.uniform(5.0, 12.0, n_samples).round(2)
    conductivity    = rng.integers(200, 600, n_samples)

    # Variable respuesta binaria basada en pH
    ph_category = (ph >= 7.0).astype(int)   # 1 = Neutro/Alcalino, 0 = Ácido

    df = pd.DataFrame({
        "ph"              : ph,
        "temperature_c"   : temperature,
        "turbidity_ntu"   : turbidity,
        "dissolved_oxygen": dissolved_oxygen,
        "conductivity_us" : conductivity,
        "ph_category"     : ph_category,
    })

    return df


if __name__ == "__main__":
    df = generate_water_quality_data()
    out_path = "data/synthetic_water_quality.csv"
    df.to_csv(out_path, index=False)
    print(f"Dataset generado: {out_path}  ({len(df)} filas)")
    print(df.head())
    print("\nDistribución ph_category:")
    print(df["ph_category"].value_counts())
