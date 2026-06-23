"""
tabs/contextoproblema.py
Pestaña 1 – Contexto del Problema e Impacto Empresarial
"""

import dash_bootstrap_components as dbc
from dash import html

# ───────────────────────────────────────────────────────────────
# Colores
# ───────────────────────────────────────────────────────────────

BLUE = "#AED9E0"
GREEN = "#B5EAD7"
YELLOW = "#FFDAC1"
PINK = "#FFB7B2"
PURPLE = "#C7CEEA"

CARD_STYLE = {
    "border": "none",
    "borderRadius": "16px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
}


def _kpi_card(icon, title, value, color):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icon, style={"fontSize": "2rem"}),
                html.H4(value, className="fw-bold mt-2 mb-0"),
                html.P(title, className="text-muted small"),
            ],
            className="text-center py-3",
        ),
        style={**CARD_STYLE, "backgroundColor": color},
    )


def layout():

    return html.Div(

        [

            dbc.Row(

                dbc.Col(

                    [

                        html.H2(
                            "💧 Predicción de la Calidad del Agua mediante Machine Learning",
                            className="fw-bold",
                            style={"color": "#2c3e50"},
                        ),

                        html.P(
                            "Este dashboard presenta el desarrollo de un modelo de Machine Learning "
                            "para clasificar muestras de agua según su categoría de pH utilizando "
                            "variables fisicoquímicas como temperatura, turbidez, oxígeno disuelto "
                            "y conductividad.",
                            className="text-muted",
                        ),

                        html.Hr(),

                    ]

                )

            ),

            dbc.Row(

                [

                    dbc.Col(
                        _kpi_card("🌍", "Personas sin agua segura", "2.2 B", BLUE),
                        md=3,
                    ),

                    dbc.Col(
                        _kpi_card("⚠️", "Muertes anuales", "1.4 M", PINK),
                        md=3,
                    ),

                    dbc.Col(
                        _kpi_card("🏭", "Sectores impactados", "4+", YELLOW),
                        md=3,
                    ),

                    dbc.Col(
                        _kpi_card("🤖", "Modelo ML", "Logística", GREEN),
                        md=3,
                    ),

                ],

                className="mb-4 g-3",

            ),

            dbc.Row(

                [

                    dbc.Col(

                        dbc.Card(

                            [

                                dbc.CardHeader(

                                    html.H5(
                                        "🔬 ¿Por qué importa el pH?",
                                        className="fw-bold mb-0",
                                    )

                                ),

                                dbc.CardBody(

                                    [

                                        html.P(
                                            "El pH representa el nivel de acidez o alcalinidad del agua. "
                                            "Es uno de los indicadores más importantes para evaluar su calidad."
                                        ),

                                        html.P(
                                            "Un pH fuera del rango recomendado puede afectar la salud humana, "
                                            "provocar corrosión en tuberías y alterar los ecosistemas acuáticos."
                                        ),

                                        html.Ul(

                                            [

                                                html.Li(
                                                    "pH < 6.5: agua ácida."
                                                ),

                                                html.Li(
                                                    "pH entre 6.5 y 8.5: rango recomendado."
                                                ),

                                                html.Li(
                                                    "pH > 8.5: agua alcalina."
                                                ),

                                            ]

                                        ),

                                    ]

                                ),

                            ],

                            style=CARD_STYLE,

                        ),

                        md=6,

                    ),
                                        dbc.Col(

                        dbc.Card(

                            [

                                dbc.CardHeader(

                                    html.H5(
                                        "🏢 Impacto Empresarial",
                                        className="fw-bold mb-0",
                                    )

                                ),

                                dbc.CardBody(

                                    [

                                        html.P(
                                            "El uso de modelos predictivos permite anticipar cambios "
                                            "en la calidad del agua, facilitando la toma de decisiones "
                                            "y reduciendo tiempos de respuesta."
                                        ),

                                        dbc.ListGroup(

                                            [

                                                dbc.ListGroupItem(
                                                    "🚰 Empresas de acueducto: monitoreo continuo de la calidad del agua."
                                                ),

                                                dbc.ListGroupItem(
                                                    "🏭 Industria: prevención de corrosión e incrustaciones."
                                                ),

                                                dbc.ListGroupItem(
                                                    "🌱 Gestión ambiental: seguimiento de cuerpos de agua."
                                                ),

                                                dbc.ListGroupItem(
                                                    "🐟 Acuicultura: mantenimiento de condiciones óptimas."
                                                ),

                                                dbc.ListGroupItem(
                                                    "🧪 Laboratorios: apoyo al control de calidad."
                                                ),

                                            ],

                                            flush=True,

                                        ),

                                    ]

                                ),

                            ],

                            style=CARD_STYLE,

                        ),

                        md=6,

                    ),

                ],

                className="mb-4 g-3",

            ),

            dbc.Row(

                dbc.Col(

                    dbc.Card(

                        [

                            dbc.CardHeader(

                                html.H5(
                                    "⚙️ Metodología del Proyecto",
                                    className="fw-bold mb-0",
                                )

                            ),

                            dbc.CardBody(

                                [

                                    html.P(
                                        "Para desarrollar el modelo predictivo se siguió una metodología "
                                        "de Ciencia de Datos que permitió transformar los datos en un "
                                        "modelo de clasificación confiable."
                                    ),

                                    html.Br(),

                                    dbc.Row(

                                        [

                                            dbc.Col(

                                                [

                                                    html.H2("📊"),

                                                    html.H5("1. Preparación"),

                                                    html.P(
                                                        "Revisión del conjunto de datos, tratamiento de valores "
                                                        "faltantes y análisis de las variables."
                                                    ),

                                                ],

                                                md=4,

                                            ),

                                            dbc.Col(

                                                [

                                                    html.H2("📈"),

                                                    html.H5("2. Análisis Exploratorio"),

                                                    html.P(
                                                        "Se exploraron distribuciones, correlaciones y "
                                                        "estadísticos descriptivos."
                                                    ),

                                                ],

                                                md=4,

                                            ),

                                            dbc.Col(

                                                [

                                                    html.H2("⚖️"),

                                                    html.H5("3. Balanceo (SMOTE)"),

                                                    html.P(
                                                        "Se aplicó SMOTE para equilibrar las clases de la "
                                                        "variable objetivo antes del entrenamiento."
                                                    ),

                                                ],

                                                md=4,

                                            ),

                                        ],

                                        className="mb-4",

                                    ),

                                    dbc.Row(

                                        [

                                            dbc.Col(

                                                [

                                                    html.H2("🧠"),

                                                    html.H5("4. Entrenamiento"),

                                                    html.P(
                                                        "Se entrenó un modelo de Regresión Logística "
                                                        "utilizando el conjunto de entrenamiento balanceado."
                                                    ),

                                                ],

                                                md=6,

                                            ),

                                            dbc.Col(

                                                [

                                                    html.H2("📉"),

                                                    html.H5("5. Evaluación"),

                                                    html.P(
                                                        "El modelo fue evaluado mediante Accuracy, Precision, "
                                                        "Recall, F1-Score, Curva ROC y Matriz de Confusión."
                                                    ),

                                                ],

                                                md=6,

                                            ),

                                        ]

                                    ),

                                ]

                            ),

                        ],

                        style=CARD_STYLE,

                    )

                ),

                className="mb-4",

            ),
                        dbc.Row(

                dbc.Col(

                    dbc.Card(

                        [

                            dbc.CardHeader(

                                html.H5(
                                    "📋 Variables del Dataset",
                                    className="fw-bold mb-0",
                                )

                            ),

                            dbc.CardBody(

                                dbc.Table(

                                    [

                                        html.Thead(

                                            html.Tr(

                                                [

                                                    html.Th("Variable"),
                                                    html.Th("Unidad"),
                                                    html.Th("Rango"),
                                                    html.Th("Rol"),

                                                ]

                                            )

                                        ),

                                        html.Tbody(

                                            [

                                                html.Tr(

                                                    [

                                                        html.Td("Temperatura"),
                                                        html.Td("°C"),
                                                        html.Td("15 - 35"),
                                                        html.Td("Predictora"),

                                                    ]

                                                ),

                                                html.Tr(

                                                    [

                                                        html.Td("Turbidez"),
                                                        html.Td("NTU"),
                                                        html.Td("0.5 - 10"),
                                                        html.Td("Predictora"),

                                                    ]

                                                ),

                                                html.Tr(

                                                    [

                                                        html.Td("Oxígeno Disuelto"),
                                                        html.Td("mg/L"),
                                                        html.Td("5 - 12"),
                                                        html.Td("Predictora"),

                                                    ]

                                                ),

                                                html.Tr(

                                                    [

                                                        html.Td("Conductividad"),
                                                        html.Td("µS/cm"),
                                                        html.Td("200 - 600"),
                                                        html.Td("Predictora"),

                                                    ]

                                                ),

                                                html.Tr(

                                                    [

                                                        html.Td("Categoría de pH"),
                                                        html.Td("-"),
                                                        html.Td("Ácido / Neutro-Alcalino"),
                                                        html.Td("Variable objetivo"),

                                                    ]

                                                ),

                                            ]

                                        ),

                                    ],

                                    bordered=True,
                                    striped=True,
                                    hover=True,
                                    responsive=True,
                                    className="mb-0",

                                )

                            ),

                        ],

                        style=CARD_STYLE,

                    )

                )

            ),

        ],

        style={"padding": "24px"},

    )