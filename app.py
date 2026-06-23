"""
app.py
Archivo principal del Dashboard de Calidad del Agua.
Arquitectura modular: cada pestaña importa su layout desde /tabs/
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# ── Importar layouts de cada pestaña ─────────────────────────────────────────
from tabs.contextoproblema import layout as layout_contexto
from tabs.eda               import layout as layout_eda
from tabs.metodologia       import layout as layout_metodologia
from tabs.metricasmodelo    import layout as layout_metricas
from tabs.prediccion        import layout as layout_prediccion
from tabs.prediccion        import register_callbacks

# ── Inicializar la app ────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap",
    ],
    suppress_callback_exceptions=True,
    title="💧 Water Quality Dashboard",
)
server = app.server  # para Gunicorn / despliegue

# ── Paleta y estilos globales ─────────────────────────────────────────────────
NAVBAR_STYLE = {
    "background"  : "linear-gradient(135deg, #AED9E0 0%, #B5EAD7 100%)",
    "boxShadow"   : "0 2px 8px rgba(0,0,0,0.12)",
    "borderBottom": "none",
}
TAB_STYLE = {
    "fontWeight"    : "600",
    "fontSize"      : "0.85rem",
    "padding"       : "10px 18px",
    "borderRadius"  : "8px 8px 0 0",
    "border"        : "none",
    "color"         : "#555",
    "backgroundColor": "#f0f4f7",
}
TAB_SELECTED_STYLE = {
    **TAB_STYLE,
    "backgroundColor": "#ffffff",
    "color"          : "#2c3e50",
    "borderTop"      : "3px solid #AED9E0",
}

# ── Layout principal ──────────────────────────────────────────────────────────
app.layout = html.Div([

    # Navbar
    dbc.Navbar(
        dbc.Container([
            html.Span("💧", style={"fontSize": "1.8rem", "marginRight": "10px"}),
            dbc.NavbarBrand("Water Quality Dashboard",
                            style={"fontWeight": "700",
                                   "fontSize"  : "1.25rem",
                                   "color"     : "#2c3e50"}),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink(
                    "🌐 OMS Water Quality",
                    href="https://www.who.int/news-room/fact-sheets/detail/drinking-water",
                    target="_blank",
                    style={"color": "#2c3e50", "fontWeight": "500", "fontSize": "0.85rem"},
                )),
            ], className="ms-auto"),
        ], fluid=True),
        style=NAVBAR_STYLE, className="mb-0 py-2",
    ),

    # Tabs de navegación
    dbc.Container([
        dcc.Tabs(
            id="main-tabs",
            value="tab-contexto",
            children=[
                dcc.Tab(label="🏠 Contexto",    value="tab-contexto",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="📊 EDA",         value="tab-eda",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="🔬 Metodología", value="tab-metodologia",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="📈 Métricas",    value="tab-metricas",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                dcc.Tab(label="🔮 Predicción",  value="tab-prediccion",
                        style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
            ],
            style={"marginTop": "16px", "border": "none"},
            colors={"border": "transparent", "primary": "#AED9E0",
                    "background": "transparent"},
        ),

        # Contenedor del contenido de cada pestaña
        html.Div(id="tab-content",
                 style={"backgroundColor": "#f8fafc",
                        "minHeight"      : "calc(100vh - 120px)",
                        "borderRadius"   : "0 0 12px 12px",
                        "boxShadow"      : "0 2px 8px rgba(0,0,0,0.06)"}),
    ], fluid=True, style={"padding": "0 24px"}),

], style={"backgroundColor": "#f0f4f7", "minHeight": "100vh",
          "fontFamily": "'Segoe UI', sans-serif"})


# ── Callback principal: cambio de pestaña ─────────────────────────────────────
@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
)
def render_tab(tab: str):
    """Renderiza el layout correspondiente a la pestaña seleccionada."""
    if tab == "tab-contexto":
        return layout_contexto()
    elif tab == "tab-eda":
        return layout_eda()
    elif tab == "tab-metodologia":
        return layout_metodologia()
    elif tab == "tab-metricas":
        return layout_metricas()
    elif tab == "tab-prediccion":
        return layout_prediccion()
    return html.Div("Pestaña no encontrada.")


# ── Registrar callbacks de predicción ────────────────────────────────────────
register_callbacks(app)

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
