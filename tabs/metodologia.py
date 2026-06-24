"""
tabs/metodologia.py
Pestaña 3 – Metodología: descripción del dataset y del modelo
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

CARD_STYLE = {
    "border"      : "none",
    "borderRadius": "16px",
    "boxShadow"   : "0 4px 12px rgba(0,0,0,0.08)",
}
PASTEL = ["#AED9E0", "#FFB7B2", "#B5EAD7", "#FFDAC1", "#C7CEEA"]


def _pipeline_diagram() -> go.Figure:
    """Diagrama de flujo del pipeline de ML."""

    steps = [
        "Datos CSV",
        "Limpieza",
        "Balanceo\n(RandomOverSampler)",
        "Train/Test",
        "Random\nForest",
        "Evaluación",
        "Predicción"
    ]
    x_pos  = list(range(len(steps)))
    colors = PASTEL * 2

    fig = go.Figure()
    for i, (step, color) in enumerate(zip(steps, colors)):
        fig.add_shape(type="rect",
                      x0=i - 0.4, x1=i + 0.4, y0=-0.3, y1=0.3,
                      fillcolor=color, line_color="#999", line_width=1,
                      layer="below")
        if i < len(steps) - 1:
            fig.add_annotation(x=i + 0.5, y=0,
                               ax=i + 0.41, ay=0,
                               xref="x", yref="y",
                               axref="x", ayref="y",
                               arrowhead=2, arrowsize=1.5,
                               arrowcolor="#555")
        fig.add_annotation(x=i, y=0, text=f"<b>{step}</b>",
                           showarrow=False, font=dict(size=10))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-0.6, len(steps) - 0.4]),
        yaxis=dict(visible=False, range=[-0.7, 0.7]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        height=160,
    )
    return fig


def layout() -> html.Div:
    """Layout de la pestaña Metodología."""
    return html.Div([

        # ── Título ────────────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.H2("🔬 Metodología", className="fw-bold mb-1",
                    style={"color": "#2c3e50"}),
            html.P("Descripción del dataset real utilizado y del modelo "
                   "de machine learning implementado.", className="text-muted"),
            html.Hr(),
        ]), className="mb-4"),

        # ── Dataset ───────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("📂 Dataset: Water Quality Testing",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P([html.Strong("Fuente: "), "Dataset real de calidad del agua."]),
                            html.P([
    html.Strong("Registros originales: "),
    "500 muestras."
]),

html.P([
    html.Strong("Preprocesamiento: "),
    "Se realizó limpieza de datos, tratamiento de valores faltantes y balanceo de clases mediante RandomOverSampler antes del entrenamiento de los modelos."
]),
                            html.P([html.Strong("Variables: "), "5 fisicoquímicas + 1 objetivo (pH)."]),
                            html.P([html.Strong("Variable respuesta: "),
                                    "pH categorizado como ",
                                    html.Code("Ácido"), " (< 7.0) o ",
                                    html.Code("Neutro/Alcalino"), " (≥ 7.0)."]),
                        ], md=6),
                        dbc.Col([
                            dbc.Table([
                                html.Thead(html.Tr([
                                    html.Th("Variable"), html.Th("Min"), html.Th("Max"),
                                ])),
                                html.Tbody([
                                    html.Tr([html.Td("pH"),               html.Td("6.83"), html.Td("7.48")]),
                                    html.Tr([html.Td("Temperatura (°C)"), html.Td("15.1"), html.Td("35.0")]),
                                    html.Tr([html.Td("Turbidez (NTU)"),   html.Td("0.5"),  html.Td("9.9")]),
                                    html.Tr([html.Td("O₂ Disuelto"),      html.Td("5.0"),  html.Td("12.0")]),
                                    html.Tr([html.Td("Conductividad"),    html.Td("200"),  html.Td("600")]),
                                ])
                            ], bordered=True, striped=True,
                               hover=True, responsive=True, className="mb-0")
                        ], md=6),
                    ])
                ])
            ], style=CARD_STYLE)),
        ], className="mb-4 g-3"),

        # ── Pipeline de ML ────────────────────────────────────────────────────
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H5("⚙️ Pipeline de Machine Learning",
                                   className="mb-0 fw-bold")),
            dbc.CardBody(
                dcc.Graph(figure=_pipeline_diagram(), config={"displayModeBar": False})
            )
        ], style=CARD_STYLE)), className="mb-4"),

        # ── Modelo ────────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("🧠 Random Forest",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    html.P(
    "Se entrenaron cinco algoritmos de clasificación (Regresión Logística, Árbol de Decisión, Random Forest, SVM y KNN). "
    "Tras comparar su desempeño mediante Accuracy, Precision, Recall, F1-score y validación cruzada estratificada, "
    "Random Forest fue seleccionado como modelo final al obtener el mejor rendimiento y una alta capacidad de generalización."
),
                    
                    html.H6("Configuración:", className="fw-bold mt-3"),
    dbc.ListGroup([
    dbc.ListGroupItem("Balanceo de clases: RandomOverSampler"),
    dbc.ListGroupItem("Modelo final: Random Forest"),
    dbc.ListGroupItem("Número de árboles: 100"),
    dbc.ListGroupItem("Criterio: Gini"),
    dbc.ListGroupItem("Validación cruzada: Stratified K-Fold (k=5)"),
    dbc.ListGroupItem("División entrenamiento/prueba: 75% / 25%"),
], flush=True),
html.H6("¿Por qué aplicar RandomOverSampler?", className="fw-bold mt-4"),

html.P(
    "Inicialmente la variable objetivo presentaba un desbalance entre las clases. "
    "Para evitar que el modelo favoreciera la clase mayoritaria se aplicó "
    "RandomOverSampler, equilibrando el número de muestras de cada clase antes del entrenamiento de los modelos."
),
                ])
            ], style=CARD_STYLE), md=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("🎯 ¿Por qué Random Forest?",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    dbc.ListGroup([
    dbc.ListGroupItem([
        html.Strong("✅ Mayor precisión: "),
        "Obtuvo el mejor desempeño entre los modelos evaluados."
    ]),
    dbc.ListGroupItem([
        html.Strong("✅ Robusto: "),
        "Reduce el sobreajuste al combinar múltiples árboles de decisión."
    ]),
    dbc.ListGroupItem([
        html.Strong("✅ Generalización: "),
        "Presentó un excelente rendimiento durante la validación cruzada."
    ]),
    dbc.ListGroupItem([
        html.Strong("✅ Manejo de variables: "),
        "No requiere normalización previa de los datos."
    ]),
    dbc.ListGroupItem([
        html.Strong("✅ Modelo seleccionado: "),
        "Fue elegido como modelo final del proyecto por obtener el mejor desempeño."
    ]),
], flush=True),

html.Hr(),

html.P([
    html.Strong("Resultado de la validación cruzada:"),
    html.Br(),
    "F1-score promedio: 0.9646",
    html.Br(),
    "Desviación estándar: 0.0117"
]),
                    html.Hr(),
                    html.P([
                        html.Strong("Clases del modelo: "),
                        html.Span("0 = Ácido (pH < 7.0)  ",
                                  style={"color": "#e74c3c", "fontWeight": "600"}),
                        html.Span("1 = Neutro/Alcalino (pH ≥ 7.0)",
                                  style={"color": "#27ae60", "fontWeight": "600"}),
                    ], className="mt-3"),
                ])
            ], style=CARD_STYLE), md=6),
        ], className="mb-4 g-3"),

    ], style={"padding": "24px"})
