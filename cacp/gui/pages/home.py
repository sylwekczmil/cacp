import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Content([
    html.Div("Hello")
])
