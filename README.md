# 💧 Water Quality Dashboard

Dashboard interactivo para la predicción de la calidad del agua mediante
**Machine Learning**, desarrollado con **Python**, **Dash** y
**Plotly**.

El proyecto implementa un modelo de **Regresión Logística** entrenado
sobre un conjunto de datos balanceado mediante **SMOTE**, permitiendo
clasificar muestras de agua en función de sus características
fisicoquímicas.

------------------------------------------------------------------------

## 📌 Objetivos

-   Analizar la calidad del agua mediante técnicas de Análisis
    Exploratorio de Datos (EDA).
-   Construir un modelo de Machine Learning para clasificar muestras de
    agua.
-   Visualizar métricas de desempeño del modelo.
-   Permitir realizar predicciones de nuevas muestras mediante una
    interfaz interactiva.

## 🚀 Tecnologías utilizadas

-   Python 3
-   Dash
-   Plotly
-   Dash Bootstrap Components
-   Pandas
-   NumPy
-   Scikit-Learn
-   Imbalanced-Learn (SMOTE)
-   Joblib

## 📂 Estructura del proyecto

``` text
water_quality_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
├── model/
│   ├── train_model.py
│   └── model.pkl
├── tabs/
│   ├── contextoproblema.py
│   ├── eda.py
│   ├── metodologia.py
│   ├── metricasmodelo.py
│   └── prediccion.py
└── assets/
```

## 📊 Dashboard

1.  **Contexto del problema**
2.  **Análisis Exploratorio de Datos (EDA)**
3.  **Metodología**
4.  **Métricas del Modelo**
5.  **Predicción Interactiva**

## 🤖 Modelo de Machine Learning

Se implementó un modelo de **Regresión Logística** utilizando **SMOTE**
para balancear las clases antes del entrenamiento.

### Métricas evaluadas

-   Accuracy
-   Precision
-   Recall
-   F1-Score
-   ROC-AUC
-   Curva ROC
-   Matriz de Confusión

## ▶️ Instalación

``` bash
git clone https://github.com/tu_usuario/water_quality_dashboard.git
cd water_quality_dashboard

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Entrenar el modelo

``` bash
python model/train_model.py
```

## ▶️ Ejecutar el dashboard

``` bash
python app.py
```

Abrir en el navegador:

    http://127.0.0.1:8050

## 👩‍💻 Autora

**Nicolle Mendoza**

Proyecto académico de Ciencia de Datos y Machine Learning aplicado a la
predicción de la calidad del agua.

## 📄 Licencia

Proyecto con fines académicos y educativos.
