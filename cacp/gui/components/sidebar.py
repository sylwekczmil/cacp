import dash_bootstrap_components as dbc
from dash import html


def sidebar_component():
    return html.Div(
        [
            html.H2(dbc.NavLink("CACP", href="/", active="exact"), className="display-4"),
            html.Hr(),
            html.P(
                "Classification Algorithms Comparison Pipeline", className="lead"
            ),
            dbc.Nav(
                [
                    dbc.NavLink("Classifiers", href="/classifiers", active="exact"),
                    dbc.NavLink("Datasets", href="/datasets", active="exact"),
                    dbc.NavLink("Experiments", href="/experiments"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
        },
    )
