import logging

import dash_bootstrap_components as dbc
import flask
from dash import Dash, html, page_container

from cacp.gui.components.shared.sidebar import sidebar_component


def start(debug: bool = False):
    log_level = logging.INFO if debug else logging.ERROR
    flask_log = logging.getLogger('werkzeug')
    flask_log.setLevel(log_level)
    flask.cli.show_server_banner = lambda *_args, **_kwargs: None

    app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP], use_pages=True)

    app.layout = html.Div([
        sidebar_component(),
        html.Div(id="page-content", style={
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",
        }, children=[page_container])
    ])

    app.logger.setLevel(log_level)

    print("CACP stared on http://127.0.0.1:8050/")
    app.run_server(debug=debug)


if __name__ == '__main__':
    start(debug=True)
