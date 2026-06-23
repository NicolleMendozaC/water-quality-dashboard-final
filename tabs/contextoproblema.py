"""
tabs/contextoproblema.py
Pestaña 1 – Contexto del Problema e Impacto Empresarial
"""

import dash_bootstrap_components as dbc
from dash import html

# ── Paleta pastel ─────────────────────────────────────────────────────────────
BLUE   = "#AED9E0"
GREEN  = "#B5EAD7"
YELLOW = "#FFDAC1"
PINK   = "#FFB7B2"
PURPLE = "#C7CEEA"

CARD_STYLE = {
    "border"      : "none",
    "borderRadius": "16px",
    "boxShadow"   : "0 4px 12px rgba(0,0,0,0.08)",
}


def _kpi_card(icon: str, title: str, value: str, color: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody([
            html.Div(icon, style={"fontSize": "2rem"}),
            html.H4(value, className="mt-2 mb-0 fw-bold"),
            html.P(title, className="text-muted small"),
        ], className="text-center py-3"),
        style={**CARD_STYLE, "backgroundColor": color},
    )


def layout() -> html.Div:
    """Retorna el layout completo de la pestaña Contexto del Problema."""
    return html.Div([

        # ── Encabezado ────────────────────────────────────────────────────────
        dbc.Row(dbc.Col(html.Div([
            html.H2("💧 Calidad del Agua – Análisis de pH",
                    className="fw-bold mb-1", style={"color": "#2c3e50"}),
            html.P("Dashboard analítico para monitoreo y clasificación "
                   "de la calidad del agua mediante machine learning.",
                   className="text-muted"),
            html.Hr(),
        ])), className="mb-4"),

        # ── KPIs ─────────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(_kpi_card("🌍", "Personas sin agua segura", "2.2 B", BLUE),   md=3),
            dbc.Col(_kpi_card("⚠️", "Muertes anuales por agua", "1.4 M", PINK),   md=3),
            dbc.Col(_kpi_card("🏭", "Sectores afectados",       "4+",    YELLOW), md=3),
            dbc.Col(_kpi_card("📉", "Reducción de costos (ML)", "35 %",  GREEN),  md=3),
        ], className="mb-5 g-3"),

        # ── Descripción del problema ──────────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("🔬 ¿Por qué importa el pH?",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    html.P([
                        "El ", html.Strong("pH"), " es uno de los indicadores más críticos "
                        "de la calidad del agua. Un rango fuera de ", html.Strong("6.5 – 8.5"),
                        " puede comprometer la salud pública, dañar equipos industriales "
                        "y alterar ecosistemas acuáticos."
                    ]),
                    html.Ul([
                        html.Li("pH < 6.5 → agua ácida: corrosiva, potencialmente tóxica."),
                        html.Li("pH 6.5 – 8.5 → rango seguro según la OMS."),
                        html.Li("pH > 8.5 → alcalinidad elevada: sabor amargo, incrustaciones."),
                    ]),
                ])
            ], style=CARD_STYLE), md=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H5("🏢 Impacto Empresarial",
                                       className="mb-0 fw-bold")),
                dbc.CardBody([
                    html.P("La detección temprana de anomalías en el pH genera valor "
                           "en múltiples sectores:"),
                    dbc.ListGroup([
                        dbc.ListGroupItem("🚰 Acueductos: garantizar agua potable y cumplir normativa."),
                        dbc.ListGroupItem("🏭 Industria: evitar corrosión en tuberías y equipos."),
                        dbc.ListGroupItem("🐟 Acuicultura: mantener ecosistemas saludables."),
                        dbc.ListGroupItem("🧪 Laboratorios: optimizar procesos de tratamiento."),
                    ], flush=True, style={"borderRadius": "8px"}),
                ])
            ], style=CARD_STYLE), md=6),
        ], className="mb-4 g-3"),

        # ── Metodología resumida ──────────────────────────────────────────────
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H5("🤖 Solución Propuesta con ML",
                                   className="mb-0 fw-bold")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div("📊", style={"fontSize": "2.5rem"}),
                        html.H6("1. Recolección de Datos", className="fw-bold mt-1"),
                        html.P("Medición de variables fisicoquímicas: pH, temperatura, "
                               "turbidez, oxígeno disuelto y conductividad.",
                               className="small text-muted"),
                    ], md=3, className="text-center"),
                    dbc.Col([
                        html.Div("🔍", style={"fontSize": "2.5rem"}),
                        html.H6("2. Análisis Exploratorio", className="fw-bold mt-1"),
                        html.P("Visualización de distribuciones, correlaciones y "
                               "patrones para entender la naturaleza de los datos.",
                               className="small text-muted"),
                    ], md=3, className="text-center"),
                    dbc.Col([
                        html.Div("🧠", style={"fontSize": "2.5rem"}),
                        html.H6("3. Modelado Predictivo", className="fw-bold mt-1"),
                        html.P("Regresión Logística para clasificar el pH como "
                               "Ácido (< 7.0) o Neutro/Alcalino (≥ 7.0).",
                               className="small text-muted"),
                    ], md=3, className="text-center"),
                    dbc.Col([
                        html.Div("✅", style={"fontSize": "2.5rem"}),
                        html.H6("4. Predicción en Tiempo Real", className="fw-bold mt-1"),
                        html.P("Formulario interactivo para predecir la categoría "
                               "de una nueva muestra de agua.",
                               className="small text-muted"),
                    ], md=3, className="text-center"),
                ])
            ])
        ], style=CARD_STYLE)), className="mb-4"),

        # ── Variables del dataset ─────────────────────────────────────────────
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H5("📋 Variables del Dataset",
                                   className="mb-0 fw-bold")),
            dbc.CardBody(
                dbc.Table([
                    html.Thead(html.Tr([
                        html.Th("Variable"), html.Th("Unidad"),
                        html.Th("Rango Típico"), html.Th("Rol"),
                    ])),
                    html.Tbody([
                        html.Tr([html.Td("pH"),               html.Td("adimensional"),
                                 html.Td("6.5 – 8.5"),        html.Td("🎯 Variable respuesta")]),
                        html.Tr([html.Td("Temperatura"),      html.Td("°C"),
                                 html.Td("15 – 35"),          html.Td("Predictora")]),
                        html.Tr([html.Td("Turbidez"),         html.Td("NTU"),
                                 html.Td("0.5 – 10"),         html.Td("Predictora")]),
                        html.Tr([html.Td("Oxígeno Disuelto"), html.Td("mg/L"),
                                 html.Td("5 – 12"),           html.Td("Predictora")]),
                        html.Tr([html.Td("Conductividad"),    html.Td("µS/cm"),
                                 html.Td("200 – 600"),        html.Td("Predictora")]),
                    ]),
                ], bordered=True, hover=True, responsive=True, striped=True,
                   className="mb-0")
            )
        ], style=CARD_STYLE))),

    ], style={"padding": "24px"})
