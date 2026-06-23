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
    "Balanceo\n(SMOTE)",
    "Train/Test",
    "StandardScaler",
    "Regresión\nLogística",
    "Evaluación"
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
    "Se realizó limpieza de datos, tratamiento de valores faltantes y balanceo de clases mediante la técnica SMOTE antes del entrenamiento del modelo."
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
                dbc.CardHeader(html.H5("🧠 Regresión Logística",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    html.P(
    "Se entrenó un modelo de Regresión Logística utilizando un conjunto de datos balanceado mediante SMOTE. "
    "El objetivo fue clasificar las muestras de agua como Ácidas o Neutro/Alcalinas reduciendo el sesgo provocado por el desbalance de clases."
),
                    html.H6("Función Sigmoide:", className="fw-bold mt-3"),
                    html.Div([
                        html.Code("P(y=1|X) = 1 / (1 + e^(-z))",
                                  style={"fontSize": "1.1rem",
                                         "backgroundColor": "#f0f4f8",
                                         "padding": "8px 14px",
                                         "borderRadius": "8px",
                                         "display": "block"}),
                        html.Small("donde  z = β₀ + β₁·pH + β₂·Temp + β₃·Turbidez + β₄·O₂ + β₅·Cond.",
                                   className="text-muted d-block mt-2"),
                    ]),
                    html.H6("Configuración:", className="fw-bold mt-3"),
                    dbc.ListGroup([
    dbc.ListGroupItem("Balanceo de clases: SMOTE"),
    dbc.ListGroupItem("Normalización: StandardScaler"),
    dbc.ListGroupItem("Modelo: Regresión Logística"),
    dbc.ListGroupItem("Solver: lbfgs"),
    dbc.ListGroupItem("Máximo de iteraciones: 500"),
    dbc.ListGroupItem("División entrenamiento/prueba: 75% / 25%"),
], flush=True),
html.H6("¿Por qué aplicar SMOTE?", className="fw-bold mt-4"),

html.P(
    "Inicialmente la variable objetivo presentaba un desbalance entre las clases. "
    "Para evitar que el modelo favoreciera la clase mayoritaria se aplicó la técnica "
    "SMOTE (Synthetic Minority Over-sampling Technique), generando nuevas muestras "
    "sintéticas de la clase minoritaria antes del entrenamiento."
),
                ])
            ], style=CARD_STYLE), md=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("🎯 ¿Por qué Regresión Logística?",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Strong("✅ Interpretable: "),
                            "Los coeficientes revelan el impacto de cada variable."
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("✅ Eficiente: "),
                            "Ideal para datasets pequeños/medianos como el nuestro."
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("✅ Probabilístico: "),
                            "Entrega la probabilidad de cada clase, no solo la etiqueta."
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("✅ Estable: "),
                            "Converge rápidamente con datos normalizados."
                        ]),
                        dbc.ListGroupItem([
                            html.Strong("✅ Línea base sólida: "),
                            "Referencia clara antes de modelos más complejos."
                        ]),
                    ], flush=True),
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
