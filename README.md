# 💧 Dashboard de Calidad del Agua

**Predicción de la categoría de pH del agua mediante Machine Learning**, con un
dashboard interactivo construido en Dash y un análisis completo documentado en
Jupyter Book.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.17-008DE4?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Jupyter Book](https://img.shields.io/badge/Jupyter%20Book-1.0-F37726?logo=jupyter&logoColor=white)](https://jupyterbook.org/)

---

## Demo en vivo

| | |
|---|---|
| 📊 **Dashboard interactivo** | [water-quality-dashboard-final.onrender.com](https://water-quality-dashboard-final.onrender.com) |
| 📘 **Jupyter Book (EDA y modelo)** | [nicollemendozac.github.io/water-quality-dashboard-final/intro.html](https://nicollemendozac.github.io/water-quality-dashboard-final/intro.html) |

> El enlace del dashboard se actualiza una vez completado el despliegue en Render — ver sección [Despliegue](#despliegue).

---

## Descripción del proyecto

El pH es uno de los indicadores más críticos de la calidad del agua: valores
fuera del rango seguro (6.5 – 8.5) pueden afectar la salud pública, dañar
infraestructura industrial y alterar ecosistemas acuáticos.

Este proyecto:

- Realiza un **análisis exploratorio de datos (EDA)** sobre 500 muestras reales
  de calidad del agua (pH, temperatura, turbidez, oxígeno disuelto y
  conductividad).
- Entrena y compara **cinco algoritmos de clasificación** (Regresión
  Logística, Árbol de Decisión, Random Forest, SVM y KNN) mediante validación
  cruzada estratificada, y selecciona **Random Forest** como modelo final por
  su mejor desempeño y estabilidad.
- Expone el modelo en un **dashboard interactivo en Dash**, donde se puede
  simular cualquier combinación de variables y obtener la predicción en
  tiempo real.
- Documenta todo el proceso —EDA, metodología, comparación de modelos y
  métricas— en un **Jupyter Book** publicado con GitHub Pages.

## Estructura del repositorio

```
water-quality-dashboard-final/
├── app.py                     # Punto de entrada del dashboard Dash
├── requirements.txt           # Dependencias del dashboard
├── assets/
│   └── custom.css             # Estilos personalizados
├── tabs/                      # Una pestaña del dashboard por módulo
│   ├── contextoproblema.py
│   ├── eda.py
│   ├── metodologia.py
│   ├── metricasmodelo.py
│   └── prediccion.py
├── data/
│   ├── Water_Quality_Testing.csv      # Dataset real (500 muestras)
│   └── synthetic_water_quality.csv    # Dataset sintético balanceado (entrenamiento)
├── model/
│   ├── train_model.py          # Script de entrenamiento
│   └── model.pkl                # Pipeline entrenado (scaler + Random Forest)
├── notebooks/
│   └── EDA_Calidad_Agua_2_0.ipynb   # Notebook fuente del Jupyter Book
├── intro.md                    # Portada del Jupyter Book
├── _config.yml                 # Configuración del Jupyter Book
├── _toc.yml                    # Tabla de contenidos del Jupyter Book
└── docs/                       # HTML generado del Jupyter Book (servido por GitHub Pages)
```

## Tecnologías utilizadas

| Categoría | Herramientas |
|---|---|
| Dashboard | Dash, Dash Bootstrap Components, Plotly |
| Modelado | scikit-learn (Random Forest, Regresión Logística, Árbol de Decisión, SVM, KNN), imbalanced-learn (`RandomOverSampler`), joblib |
| Análisis y documentación | Jupyter Book, pandas, NumPy, Matplotlib, Seaborn, SciPy |
| Despliegue | Render (dashboard) · GitHub Pages (Jupyter Book) |

## Metodología

```
Datos CSV → Limpieza → Variable objetivo (pH ≥ 7.0) → Balanceo de clases
          (RandomOverSampler) → Train/Test Split (75/25, estratificado)
          → StandardScaler → Comparación de 5 modelos → Validación cruzada
          → Selección del modelo final (Random Forest)
```

El dataset original está fuertemente desbalanceado (98% Neutro/Alcalino vs.
2% Ácido), por lo que se aplicó **`RandomOverSampler`** antes de entrenar,
para evitar que los modelos favorecieran la clase mayoritaria.

Se compararon cinco algoritmos de clasificación con los mismos conjuntos de
entrenamiento y prueba, y se validó su estabilidad con **validación cruzada
estratificada (5 folds)**:

| Modelo | Accuracy | Precision | Recall | F1-Score | F1 (cross-val) |
|---|---|---|---|---|---|
| **Random Forest** ⭐ | 100% | 100% | 100% | 100% | **99.80% ± 0.25%** |
| Árbol de Decisión | 99.59% | 100% | 99.18% | 99.59% | 99.39% ± 0.20% |
| KNN | 99.59% | 100% | 99.18% | 99.59% | 98.88% ± 0.38% |
| Regresión Logística | 93.47% | 92.74% | 94.26% | 93.50% | 88.98% ± 1.05% |
| SVM | 99.59% | 100% | 99.18% | 99.59% | 50.10% ± 1.84% |

**Random Forest** fue seleccionado como modelo final: obtuvo el mejor F1-score
promedio en validación cruzada (99.80%) con la menor desviación estándar
(±0.25%), lo que indica un desempeño alto y consistente entre particiones —no
solo un buen resultado puntual en un único split de prueba.

El detalle completo del EDA, el proceso de balanceo, la comparación de los
cinco modelos y la interpretación de cada métrica está documentado en el
[Jupyter Book](https://nicollemendozac.github.io/water-quality-dashboard-final/intro.html).

## Cómo ejecutar el dashboard localmente

```bash
git clone https://github.com/NicolleMendozaC/water-quality-dashboard-final.git
cd water-quality-dashboard-final
pip install -r requirements.txt

# (Opcional) Reentrenar el modelo (Random Forest) desde cero
python model/train_model.py

# Levantar el dashboard
python app.py
```

La aplicación queda disponible en `http://127.0.0.1:8050`.

## Cómo reconstruir el Jupyter Book

```bash
pip install jupyter-book
jupyter-book build .
```

El HTML se genera en `_build/html/`. Para publicarlo en GitHub Pages desde la
carpeta `docs/`:

```bash
rm -rf docs        # o `rmdir /S /Q docs` en Windows
cp -r _build/html docs   # o `xcopy _build\html docs /E /I /H` en Windows
touch docs/.nojekyll     # evita que Jekyll ignore los assets de Sphinx
git add docs
git commit -m "Actualizar Jupyter Book"
git push origin main
```

## Despliegue

| Componente | Plataforma | Notas |
|---|---|---|
| Dashboard (`app.py`) | [Render](https://render.com) | Start command: `gunicorn app:server` — requiere agregar `gunicorn` a `requirements.txt` |
| Jupyter Book (`docs/`) | GitHub Pages | Settings → Pages → Deploy from a branch → `main` / `docs` |

## Equipo

Proyecto desarrollado para el curso **Python para Ciencia de Datos** — Grupo 4.

- Nicolle Mendoza
- Carlos Díaz
- Habib Hadechini
- Jhonatan Blanco
