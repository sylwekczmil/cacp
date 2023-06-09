import dash
import dash_bootstrap_components as dbc
from dash import html, Output, Input, State

dash.register_page(__name__, path_template="/experiment-new")

name_input = html.Div(
    [
        dbc.Label("Name", html_for="name"),
        dbc.Input(id="name", placeholder="Enter name"),
        dbc.FormText(
            "Provide name for your experiment, it should be unique.",
            color="secondary",
        ),
    ],
    className="mb-3",
)

layout = html.Div([
    name_input,
    html.Div([
        dbc.Button(
            "Run experiment", id="run-experiment-button", className="me-2"
        )
    ], className="d-flex justify-content-end align-items-center"),
    html.Div(id="output_div")
])


@dash.callback(Output('output_div', 'children'),
               [Input('run-experiment-button', 'n_clicks')],
               [State('name', 'value')],
               )
def update_output(clicks, name):
    if clicks is not None:
        print(clicks, name)
