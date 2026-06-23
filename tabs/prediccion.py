"""
tabs/prediccion.py
Pestaña 5 – Predicción Interactiva
Formulario que carga model.pkl y predice la categoría de pH de una nueva muestra.
"""

import os
import joblib
import numpy as np
from dash import dcc, html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc

CARD_STYLE = {
    "border"      : "none",
    "borderRadius": "16px",
    "boxShadow"   : "0 4px 12px rgba(0,0,0,0.08)",
}
PASTEL = ["#AED9E0", "#FFB7B2", "#B5EAD7", "#FFDAC1", "#C7CEEA"]

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")


def _slider(id_: str, label: str, min_: float, max_: float,
            step: float, value: float, color: str) -> html.Div:
    """Componente reutilizable: label + slider + display del valor actual."""
    return html.Div([
        dbc.Row([
            dbc.Col(html.Label(label, className="fw-semibold small"), width=8),
            dbc.Col(html.Span(id=f"{id_}-val",
                              children=str(value),
                              style={"fontWeight": "700",
                                     "color"     : "#2c3e50",
                                     "fontSize"  : "1rem"}),
                    width=4, className="text-end"),
        ]),
        dcc.Slider(
            id=id_, min=min_, max=max_, step=step, value=value,
            marks={min_: str(min_), max_: str(max_)},
            tooltip={"always_visible": False},
            className="mb-3",
        ),
    ], style={"backgroundColor": color,
              "padding": "12px 16px",
              "borderRadius": "10px",
              "marginBottom": "12px"})


def layout() -> html.Div:
    """Layout de la pestaña Predicción Interactiva."""
    model_loaded = os.path.exists(MODEL_PATH)

    return html.Div([

        # ── Título ────────────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.H2("🔮 Predicción Interactiva", className="fw-bold mb-1",
                    style={"color": "#2c3e50"}),
            html.P("Ajusta los parámetros fisicoquímicos y obtén la predicción "
                   "de la categoría de pH en tiempo real.", className="text-muted"),
            html.Hr(),
        ]), className="mb-4"),

        # ── Alerta si no hay modelo ───────────────────────────────────────────
        dbc.Alert(
            "⚠️  Modelo no entrenado. Ejecuta: python model/train_model.py",
            color="warning", is_open=not model_loaded,
            style={"borderRadius": "10px", "marginBottom": "20px"},
        ),

        dbc.Row([
            # ── Panel izquierdo: sliders ──────────────────────────────────────
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("⚙️ Parámetros de la Muestra",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    _slider("sl-temp",  "Temperatura (°C)",      15,  35,  0.1,  25.0, PASTEL[2]),
                    _slider("sl-turb",  "Turbidez (NTU)",        0.5, 10,  0.1,  3.0,  PASTEL[3]),
                    _slider("sl-do",    "Oxígeno Disuelto (mg/L)", 5, 12,  0.1,  8.0,  PASTEL[4]),
                    _slider("sl-cond",  "Conductividad (µS/cm)", 200, 600, 5,    350,  PASTEL[1]),

                    dbc.Button("🔍 Predecir", id="btn-predict", color="primary",
                               className="w-100 mt-2",
                               style={"borderRadius": "10px",
                                      "fontWeight"  : "600",
                                      "fontSize"    : "1rem"},
                               disabled=not model_loaded),
                ])
            ], style=CARD_STYLE), md=5),

            # ── Panel derecho: resultado ──────────────────────────────────────
            dbc.Col([
                dbc.Card(dbc.CardBody(
                    html.Div(id="pred-result", children=[
                        html.Div([
                            html.Div("🔎", style={"fontSize": "4rem"}),
                            html.H4("Ajusta los parámetros y presiona",
                                    className="mt-2 text-muted"),
                            html.H4('"Predecir"', className="text-muted"),
                        ], className="text-center py-4"),
                    ])
                ), style={**CARD_STYLE, "minHeight": "280px"}),

                # Gauge de probabilidad
                dbc.Card(dbc.CardBody(
                    dcc.Graph(id="pred-gauge", config={"displayModeBar": False},
                              style={"height": "220px"})
                ), style={**CARD_STYLE, "marginTop": "16px"}),
            ], md=7),
        ], className="g-3"),

        # ── Valores de sliders (sincronizar labels) ───────────────────────────
        html.Div(id="hidden-sync", style={"display": "none"}),

    ], style={"padding": "24px"})


# ── Callbacks ─────────────────────────────────────────────────────────────────

def register_callbacks(app):
    """Registra los callbacks de la pestaña Predicción en la app Dash."""

    # Actualizar labels de sliders en tiempo real
    for id_ in ["sl-temp", "sl-turb", "sl-do", "sl-cond"]:
        @app.callback(
            Output(f"{id_}-val", "children"),
            Input(id_, "value"),
        )
        def update_label(value):
            return str(value)

    # Predicción al hacer clic en el botón
    @app.callback(
        Output("pred-result", "children"),
        Output("pred-gauge",  "figure"),
        Input("btn-predict", "n_clicks"),
        State("sl-temp", "value"),
        State("sl-turb", "value"),
        State("sl-do",   "value"),
        State("sl-cond", "value"),
        prevent_initial_call=True,
    )
    def predict(n_clicks, temp, turb, do, cond):
        if not os.path.exists(MODEL_PATH):
            return no_update, no_update

        data    = joblib.load(MODEL_PATH)
        pipeline = data["pipeline"]

        X       = np.array([[temp, turb, do, cond]])
        pred    = pipeline.predict(X)[0]
        proba   = pipeline.predict_proba(X)[0]
        prob_1  = proba[1]           # probabilidad Neutro/Alcalino

        # ── Tarjeta de resultado ──────────────────────────────────────────────
        if pred == 1:
            icon, label, bg = "✅", "Neutro / Alcalino", "#d4edda"
            text_color = "#155724"
        else:
            icon, label, bg = "⚠️", "Ácido", "#f8d7da"
            text_color = "#721c24"

        result_card = html.Div([
            html.Div(icon,  style={"fontSize": "3.5rem"}),
            html.H3(label, style={"color": text_color, "fontWeight": "700"}),
            html.P(f"Probabilidad Neutro/Alcalino: {prob_1:.1%}",
                   className="mb-1"),
            html.P(f"Probabilidad Ácido: {1 - prob_1:.1%}",
                   className="mb-0"),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Small([html.Strong("Temp: "), f"{temp} °C"]),md=4),
                dbc.Col(html.Small([html.Strong("Turb: "), f"{turb} NTU"]),md=4),
            ]),
            dbc.Row([
                dbc.Col(html.Small([html.Strong("O₂: "), f"{do} mg/L"]), md=6),
                dbc.Col(html.Small([html.Strong("Cond: "), f"{cond} µS/cm"]),md=6),
            ], className="mt-1"),
        ], className="text-center py-3",
           style={"backgroundColor": bg, "borderRadius": "12px", "padding": "20px"})

        # ── Gauge ─────────────────────────────────────────────────────────────
        gauge = go.Figure(go.Indicator(
            mode ="gauge+number+delta",
            value=prob_1 * 100,
            title={"text": "Probabilidad Neutro/Alcalino (%)"},
            delta={"reference": 50, "increasing": {"color": "#27ae60"},
                   "decreasing": {"color": "#e74c3c"}},
            gauge={
                "axis"     : {"range": [0, 100]},
                "bar"      : {"color": "#AED9E0"},
                "steps"    : [
                    {"range": [0,  50],  "color": "#FFB7B2"},
                    {"range": [50, 100], "color": "#B5EAD7"},
                ],
                "threshold": {
                    "line" : {"color": "#2c3e50", "width": 4},
                    "thickness": 0.75,
                    "value": 50,
                },
            },
            number={"suffix": "%"},
        ))
        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI, sans-serif"),
            margin=dict(t=30, b=10, l=20, r=20),
            height=200,
        )

        return result_card, gauge
