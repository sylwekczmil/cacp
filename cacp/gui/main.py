import logging

import dash_bootstrap_components as dbc
import diskcache
import flask
from dash import Dash, html
from dash import DiskcacheManager
from dash import page_container
from dash.dcc import Location

from cacp.gui.components.shared.sidebar import sidebar_component
from cacp.gui.components.shared.utils import GLOBAL_LOCATION_ID
from cacp.gui.db import DB_PATH

CACHE_PATH = DB_PATH / ".cache"
CACHE_PATH.mkdir(exist_ok=True, parents=True)
BACKGROUND_CALLBACK_MANAGER = DiskcacheManager(diskcache.Cache(CACHE_PATH))


def start(debug: bool = False, host="127.0.0.1", port=8050):
    log_level = logging.INFO if debug else logging.ERROR
    flask_log = logging.getLogger("werkzeug")
    flask_log.setLevel(log_level)
    flask.cli.show_server_banner = lambda *_args, **_kwargs: None

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP],
        use_pages=True,
        background_callback_manager=BACKGROUND_CALLBACK_MANAGER
    )
    app.layout = html.Div([
        Location(id=GLOBAL_LOCATION_ID),
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
    start(debug=True, host="127.0.0.1", port=8050)
