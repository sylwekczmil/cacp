import dash_bootstrap_components as dbc
from dash import html


def sidebar_component():
    return html.Div(
        [
            html.Div([
                html.Div([
                    html.H2(dbc.NavLink("CACP", href="/"), className="display-4"),
                    html.Hr(),
                    html.P(
                        "Classification Algorithms Comparison Pipeline", className="lead"
                    ),
                    dbc.Nav(
                        [
                            dbc.NavLink("Datasets", href="/datasets", active="exact"),
                            dbc.NavLink("Classifiers", href="/classifiers", active="exact"),
                            dbc.NavLink("Metrics", href="/metrics", active="exact"),
                            dbc.NavLink("Experiments", href="/", active="exact"),
                            html.Br(),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                ]),
                dbc.Button("Create new experiment", href="/experiment-form"),
                html.Script("runNavLinksRoutine()"),
            ],
                className="d-flex justify-content-between flex-column h-100"),
        ],
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            "backgroundColor": "#f8f9fa",
        }
    )
