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
- Entrena un modelo de **regresión logística** que clasifica el agua como
  *Ácida* o *Neutra/Alcalina* a partir de esas variables.
- Expone el modelo en un **dashboard interactivo en Dash**, donde se puede
  simular cualquier combinación de variables y obtener la predicción en
  tiempo real.
- Documenta todo el proceso —EDA, metodología y métricas— en un
  **Jupyter Book** publicado con GitHub Pages.

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
│   └── model.pkl                # Pipeline entrenado (scaler + regresión logística)
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
| Modelado | scikit-learn (regresión logística, `StandardScaler`), joblib |
| Análisis y documentación | Jupyter Book, pandas, NumPy, Matplotlib, Seaborn |
| Despliegue | Render (dashboard) · GitHub Pages (Jupyter Book) |

## Metodología

```
Datos CSV → Limpieza → Train/Test Split (75/25, estratificado)
          → StandardScaler → Regresión Logística → Evaluación
```

Se eligió la regresión logística por ser un modelo **interpretable, eficiente
y estable** en datasets pequeños/medianos — una línea base sólida antes de
considerar modelos más complejos.

**Resultados de la evaluación** (conjunto de prueba):

| Métrica | Valor |
|---|---|
| Accuracy | 98.8% |
| Precision | 99.5% |
| Recall | 98.9% |
| F1-Score | 99.2% |
| ROC-AUC | 99.98% |

El detalle completo del EDA, la metodología y la interpretación de estas
métricas está documentado en el [Jupyter Book](https://nicollemendozac.github.io/water-quality-dashboard-final/intro.html).

## Cómo ejecutar el dashboard localmente

```bash
git clone https://github.com/NicolleMendozaC/water-quality-dashboard-final.git
cd water-quality-dashboard-final
pip install -r requirements.txt

# (Opcional) Reentrenar el modelo desde cero
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
