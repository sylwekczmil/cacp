import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.Div('This is experiments page'),
    html.Div([
        dbc.Button(
            "Run new experiment", className="me-2", href="/experiment-new"
        )
    ], className="d-flex justify-content-end align-items-center"),
])
