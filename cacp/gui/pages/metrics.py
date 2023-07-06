import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H5("Custom metrics (batch, incremental)"),
    html.H5("Sklearn metrics (batch)", className="mt-4"),
    html.H5("River metrics (incremental)", className="mt-4"),
])
