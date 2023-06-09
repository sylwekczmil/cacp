import dash
from dash import html

dash.register_page(__name__, path_template="/experiment/<experiment_id>")


def layout(experiment_id=None):
    return html.Div([
        html.Div(f'This is experiment {experiment_id}'),
    ])
