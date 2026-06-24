# 💧 Water Quality Dashboard

Un dashboard interactivo para el análisis y predicción de la calidad del agua utilizando variables fisicoquímicas como pH, temperatura, turbidez, oxígeno disuelto y conductividad.

## 📌 Objetivo del proyecto
Analizar variables fisicoquímicas del agua, explorar patrones relacionados con el pH y construir un modelo de Machine Learning para clasificar la calidad del agua.

## 📊 Variables del dataset
- pH  
- Temperature (°C)  
- Turbidity (NTU)  
- Dissolved Oxygen (mg/L)  
- Conductivity (µS/cm)  
- Sample ID  

## 🧠 Modelo de Machine Learning
Variable objetivo: pH_categoria (derivada del pH)

Algoritmo: Random Forest Classifier  
Validación: Train/Test Split + Cross Validation  

## 📈 Resultados del modelo
- Train Accuracy: ~1.0  
- Test Accuracy: ~0.98–0.99  
- CV Mean: ~0.98  

## ⚠️ Nota
El alto desempeño se debe a la fuerte relación entre variables fisicoquímicas y el pH, lo que hace el problema altamente separable.

## 🛠️ Tecnologías
Python, Pandas, NumPy, Scikit-learn, Plotly, Dash, Joblib

## 🚀 Ejecución
git clone https://github.com/NicolleMendozaC/water-quality-dashboard-final.git
cd water-quality-dashboard-final
pip install -r requirements.txt
python app.py
