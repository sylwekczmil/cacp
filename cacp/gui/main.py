import logging

import dash_bootstrap_components as dbc
import diskcache
import flask
from dash import Dash, html
from dash import DiskcacheManager
from dash import page_container
from dash.dcc import Location

from cacp.gui.components.shared.sidebar import sidebar_component
from cacp.gui.db import DB_PATH


def start(debug: bool = False, host="127.0.0.1", port=8050):
    log_level = logging.INFO if debug else logging.ERROR
    flask_log = logging.getLogger("werkzeug")
    flask_log.setLevel(log_level)
    flask.cli.show_server_banner = lambda *_args, **_kwargs: None

    app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP], use_pages=True,
               background_callback_manager=DiskcacheManager(diskcache.Cache(DB_PATH / ".cache")))

    app.layout = html.Div([
        Location(id="location"),
        sidebar_component(),
        html.Div(id="page-content", style={
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",
        }, children=[page_container]),

    ])

    app.logger.setLevel(log_level)

    print(f"CACP stared on http://{host}:{port}/")
    app.run_server(debug=debug, host=host, port=port)


if __name__ == "__main__":
    start(debug=True, host="0.0.0.0", port=8050)
