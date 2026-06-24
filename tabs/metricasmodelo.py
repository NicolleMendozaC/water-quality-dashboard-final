"""
tabs/metricasmodelo.py
Pestaña 4 – Métricas del Modelo: accuracy, precision, recall, F1, ROC, matriz de confusión
"""

import os
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import dcc, html
import dash_bootstrap_components as dbc
from sklearn.metrics import roc_curve, auc

CARD_STYLE = {
    "border"      : "none",
    "borderRadius": "16px",
    "boxShadow"   : "0 4px 12px rgba(0,0,0,0.08)",
    "height"      : "100%",
}
PASTEL = ["#AED9E0", "#FFB7B2", "#B5EAD7", "#FFDAC1", "#C7CEEA"]
PLOT_CFG = {"displayModeBar": False}

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")


def _load_model() -> dict | None:
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def _badge(label: str, value: float, color: str) -> dbc.Card:
    return dbc.Card(dbc.CardBody([
        html.H3(f"{value:.1%}", className="fw-bold mb-0"),
        html.P(label, className="text-muted small mb-0"),
    ], className="text-center py-3"),
    style={**CARD_STYLE, "backgroundColor": color})


def _fig_roc(y_test: list, y_proba: list, roc_auc_val: float) -> go.Figure:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines", name=f"ROC (AUC = {roc_auc_val:.3f})",
        line=dict(color="#AED9E0", width=3),
        fill="tozeroy", fillcolor="rgba(174,217,224,0.2)",
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        line=dict(color="#aaa", width=1.5, dash="dash"),
        name="Clasificador aleatorio",
    ))
    fig.update_layout(
        title="Curva ROC",
        xaxis_title="Tasa de Falsos Positivos (FPR)",
        yaxis_title="Tasa de Verdaderos Positivos (TPR)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif"),
        legend=dict(x=0.55, y=0.1),
        margin=dict(t=50, b=30, l=30, r=20),
    )
    return fig


def _fig_cm(cm: list) -> go.Figure:
    z      = cm
    labels = ["Ácido (0)", "Neutro/Alcalino (1)"]
    text   = [[str(v) for v in row] for row in z]
    fig = go.Figure(go.Heatmap(
        z=z, x=labels, y=labels,
        colorscale=[[0, "#f8f9fa"], [1, "#AED9E0"]],
        showscale=False,
        text=text, texttemplate="<b>%{text}</b>",
        hovertemplate="Real: %{y}<br>Predicho: %{x}<br>Conteo: %{z}<extra></extra>",
    ))
    fig.update_layout(
        title="Matriz de Confusión",
        xaxis_title="Predicho",
        yaxis_title="Real",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(t=50, b=30, l=60, r=20),
    )
    return fig


def layout() -> html.Div:
    """Layout de la pestaña Métricas del Modelo."""
    data = _load_model()

    print("Modelo cargado:")
    print(data)

    if data is None:
        return html.Div([
            dbc.Alert([
                html.H4("⚠️ Modelo no encontrado", className="alert-heading"),
                html.P("Ejecuta primero: python model/train_model.py"),
            ], color="warning", style={"margin": "40px"}),
        ])

    m = data["metrics"]

    print("\n====================")
    print("MÉTRICAS CARGADAS")

    for k, v in m.items():
        if k not in ["y_test", "y_proba", "confusion_matrix"]:
            print(k, ":", v)

    print("Confusion Matrix:")
    print(m["confusion_matrix"])
    print("====================\n")

    return html.Div([

        # ── Título ────────────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.H2("📈 Métricas del Modelo", className="fw-bold mb-1",
                    style={"color": "#2c3e50"}),
            html.P(
                "Evaluación del modelo Random Forest seleccionado como modelo final tras la comparación de algoritmos y la validación cruzada.",
                className="text-muted",
            ),
            html.Hr(),
        ]), className="mb-4"),

        # ── KPI métricas ──────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(_badge("Accuracy",  m["accuracy"],  PASTEL[0]), md=3),
            dbc.Col(_badge("Precision", m["precision"], PASTEL[2]), md=3),
            dbc.Col(_badge("Recall",    m["recall"],    PASTEL[3]), md=3),
            dbc.Col(_badge("F1-Score",  m["f1"],        PASTEL[4]), md=3),
        ], className="mb-4 g-3"),

        dbc.Row(
            dbc.Col(
                dbc.Alert([
                    html.H5("✅ Modelo final: Random Forest", className="alert-heading"),
                    html.P(
                        "Después de comparar cinco algoritmos de clasificación y aplicar validación cruzada estratificada, "
                        "Random Forest fue seleccionado como modelo final por su mejor desempeño."
                    ),
                ], color="success"),
            ),
            className="mb-4",
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Span("ROC-AUC: ", className="fw-bold"),
                            html.Span(
                                f"{m['roc_auc']:.4f}",
                                style={
                                    "fontSize": "1.3rem",
                                    "color": "#2980b9",
                                    "fontWeight": "700"
                                }
                            ),
                            html.Small(
                                " — Cuanto más cercano a 1.0, mejor discrimina el modelo.",
                                className="text-muted ms-2"
                            ),
                        ])
                    ]),
                    style={**CARD_STYLE, "backgroundColor": "#EBF5FB"},
                ),
            ),
            className="mb-4"
        ),

        # ROC + CM
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(
                dcc.Graph(
                    figure=_fig_roc(m["y_test"], m["y_proba"], m["roc_auc"]),
                    config=PLOT_CFG,
                    style={"height": "380px"},
                )
            ), style=CARD_STYLE), md=7),

            dbc.Col(dbc.Card(dbc.CardBody(
                dcc.Graph(
                    figure=_fig_cm(m["confusion_matrix"]),
                    config=PLOT_CFG,
                    style={"height": "380px"},
                )
            ), style=CARD_STYLE), md=5),
        ], className="mb-4 g-3"),

        # Validación cruzada
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("🔁 Validación Cruzada", className="fw-bold"),

                        html.P([
                            html.Strong("Método: "),
                            "Stratified K-Fold (5 particiones)"
                        ]),

                        html.P([
                            html.Strong("F1-score promedio: "),
                            html.Span(
                                f"{m['cv_f1_mean']:.4f}",
                                style={
                                    "color": "#27ae60",
                                    "fontWeight": "700",
                                    "fontSize": "1.1rem"
                                }
                            )
                        ]),

                        html.P([
                            html.Strong("Desviación estándar: "),
                            f"{m['cv_f1_std']:.4f}"
                        ]),

                        html.Small(
                            "Resultados consistentes entre folds.",
                            className="text-muted"
                        )
                    ]),
                    style=CARD_STYLE
                )
            ),
            className="mb-4",
        ),

    ], style={"padding": "24px"})