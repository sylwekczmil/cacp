import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H5("Custom metrics"),
    html.H5("Sklearn metrics (BATCH)", className="mt-4"),
    html.H5("River metrics (INCREMENTAL)", className="mt-4"),
])
