"""
tabs/eda.py
Pestaña 2 – Análisis Exploratorio de Datos (EDA)
Gráficos: dona, barplot, histogramas, heatmap de correlación
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
import numpy as np

# ── Paleta pastel ─────────────────────────────────────────────────────────────
PASTEL = ["#AED9E0", "#FFB7B2", "#B5EAD7", "#FFDAC1", "#C7CEEA", "#FF9AA2"]
CARD_STYLE = {
    "border"      : "none",
    "borderRadius": "16px",
    "boxShadow"   : "0 4px 12px rgba(0,0,0,0.08)",
    "height"      : "100%",
}
PLOT_CONFIG = {"displayModeBar": False}

# ── Carga de datos ────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "Water_Quality_Testing.csv")

_RENAME = {
    "pH"                     : "ph",
    "Temperature (°C)"       : "temperature_c",
    "Turbidity (NTU)"        : "turbidity_ntu",
    "Dissolved Oxygen (mg/L)": "dissolved_oxygen",
    "Conductivity (µS/cm)"   : "conductivity_us",
}
_LABELS = {
    "ph"              : "pH",
    "temperature_c"   : "Temperatura (°C)",
    "turbidity_ntu"   : "Turbidez (NTU)",
    "dissolved_oxygen": "Oxígeno Disuelto (mg/L)",
    "conductivity_us" : "Conductividad (µS/cm)",
    "ph_category"     : "Categoría pH",
}
_NUMERIC = ["ph", "temperature_c", "turbidity_ntu",
            "dissolved_oxygen", "conductivity_us"]


def _load_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = df.rename(columns=_RENAME)

    # Utilizar la columna creada durante el preprocesamiento
    if "pH_categoria" in df.columns:
        df["ph_category"] = df["pH_categoria"].replace({
            0: "Ácido",
            1: "Neutro/Alcalino"
        })
    else:
        df["ph_category"] = df["ph"].apply(
            lambda x: "Neutro/Alcalino" if x >= 7.0 else "Ácido"
        )

    return df


# ── Funciones de gráficos ─────────────────────────────────────────────────────

def _fig_donut(df: pd.DataFrame) -> go.Figure:
    """Gráfico de dona: distribución de categorías de pH."""
    counts = df["ph_category"].value_counts().reset_index()
    counts.columns = ["Categoría", "Cantidad"]
    fig = go.Figure(go.Pie(
        labels=counts["Categoría"],
        values=counts["Cantidad"],
        hole=0.55,
        marker_colors=[PASTEL[0], PASTEL[1]],
        textinfo="percent+label",
        hovertemplate="%{label}<br>%{value} muestras<extra></extra>",
    ))
    fig.update_layout(
        title_text="Distribución de Categorías de pH",
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(t=50, b=20, l=20, r=20),
        annotations=[dict(text="pH", x=0.5, y=0.5,
                          font_size=20, showarrow=False)],
    )
    return fig


def _fig_barplot(df: pd.DataFrame) -> go.Figure:
    """Barplot: promedio de cada variable por categoría de pH."""
    means = df.groupby("ph_category")[_NUMERIC].mean().reset_index()
    fig = go.Figure()
    for i, var in enumerate(_NUMERIC):
        fig.add_trace(go.Bar(
            name=_LABELS[var],
            x=means["ph_category"],
            y=means[var],
            marker_color=PASTEL[i % len(PASTEL)],
        ))
    fig.update_layout(
        title_text="Promedio de Variables por Categoría de pH",
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=20, l=20, r=20),
        xaxis_title="Categoría de pH",
        yaxis_title="Valor Promedio",
    )
    return fig


def _fig_histograms(df: pd.DataFrame) -> list:
    """Lista de histogramas para las 5 variables numéricas."""
    figs = []
    for i, var in enumerate(_NUMERIC):
        fig = px.histogram(
            df, x=var, color="ph_category",
            nbins=25,
            color_discrete_sequence=[PASTEL[0], PASTEL[1]],
            labels={var: _LABELS[var], "ph_category": "Categoría"},
            title=f"Distribución de {_LABELS[var]}",
            barmode="overlay",
            opacity=0.75,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor ="rgba(0,0,0,0)",
            font=dict(family="Segoe UI, sans-serif"),
            margin=dict(t=50, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1),
        )
        figs.append(fig)
    return figs


def _fig_corr(df: pd.DataFrame) -> go.Figure:
    """Heatmap de correlación entre variables numéricas."""
    corr = df[_NUMERIC].corr().round(2)
    labels = [_LABELS[c] for c in corr.columns]
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale="RdBu",
        zmid=0,
        text=corr.values.round(2),
        texttemplate="%{text}",
        hovertemplate="%{y} – %{x}<br>r = %{z}<extra></extra>",
    ))
    fig.update_layout(
        title_text="Matriz de Correlación",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, sans-serif"),
        margin=dict(t=50, b=20, l=20, r=20),
    )
    return fig


# ── Layout ────────────────────────────────────────────────────────────────────

def layout() -> html.Div:
    """Retorna el layout completo del EDA."""
    df   = _load_df()
    hist = _fig_histograms(df)

    def _graph(fig_id: str, fig: go.Figure) -> dcc.Graph:
        return dcc.Graph(id=fig_id, figure=fig, config=PLOT_CONFIG,
                         style={"height": "360px"})

    return html.Div([

        # ── Título ──────────────────────────────────────────────────────────
        dbc.Row(dbc.Col(html.Div([
            html.H2("📊 Análisis Exploratorio de Datos",
                    className="fw-bold mb-1", style={"color": "#2c3e50"}),
            html.P("Exploración visual de las variables fisicoquímicas "
                   "del agua y su relación con el pH.",
                   className="text-muted"),
            html.Hr(),
        ])), className="mb-4"),

        # ── Tarjetas estadísticas ────────────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(f"{len(df)}", className="fw-bold mb-0"),
                html.P("Muestras totales", className="text-muted small"),
            ]), style={**CARD_STYLE, "backgroundColor": "#AED9E0"}), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(f"{df['ph'].mean():.2f}", className="fw-bold mb-0"),
                html.H6("(σ = " + f"{df['ph'].std():.2f})", className="text-muted"),
                html.P("pH Promedio ± Desv. Est.", className="text-muted small"),
            ]), style={**CARD_STYLE, "backgroundColor": "#B5EAD7"}), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(f"{(df['ph_category'] == 'Neutro/Alcalino').sum()}",
                        className="fw-bold mb-0"),
                html.P("Muestras Neutro/Alcalino", className="text-muted small"),
            ]), style={**CARD_STYLE, "backgroundColor": "#FFDAC1"}), md=3),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4(f"{(df['ph_category'] == 'Ácido').sum()}",
                        className="fw-bold mb-0"),
                html.P("Muestras Ácidas", className="text-muted small"),
            ]), style={**CARD_STYLE, "backgroundColor": "#FFB7B2"}), md=3),
        ], className="mb-4 g-3"),

        # ── Fila 1: Dona + Barplot ───────────────────────────────────────────
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(
                _graph("fig-donut", _fig_donut(df))
            ), style=CARD_STYLE), md=5),
            dbc.Col(dbc.Card(dbc.CardBody(
                _graph("fig-bar", _fig_barplot(df))
            ), style=CARD_STYLE), md=7),
        ], className="mb-4 g-3"),

        # ── Fila 2: Histogramas ──────────────────────────────────────────────
        dbc.Row(dbc.Col(html.H5("📈 Distribuciones por Variable",
                                 className="fw-bold mb-3"))),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(
                _graph(f"fig-hist-{i}", hist[i])
            ), style=CARD_STYLE), md=4)
            for i in range(3)
        ], className="mb-3 g-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(
                _graph(f"fig-hist-{i+3}", hist[i+3])
            ), style=CARD_STYLE), md=6)
            for i in range(2)
        ], className="mb-4 g-3"),

        # ── Fila 3: Correlación ──────────────────────────────────────────────
        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(
            _graph("fig-corr", _fig_corr(df))
        ), style=CARD_STYLE), md=12), className="mb-4 g-3"),

    ], style={"padding": "24px"})
