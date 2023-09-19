import logging

import click
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
from cacp.gui.preview import is_preview

CACHE_PATH = DB_PATH / ".cache"
CACHE_PATH.mkdir(exist_ok=True, parents=True)
BACKGROUND_CALLBACK_MANAGER = DiskcacheManager(diskcache.Cache(CACHE_PATH))


@click.command()
@click.option("--debug", "-d", is_flag=True, show_default=True, default=False, type=bool)
@click.option("--host", "-h", show_default=True, default="127.0.0.1", type=str)
@click.option("--port", "-p", show_default=True, default=8050, type=int)
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
        }, children=[page_container]),  # https://cacp.readthedocs.io/

        dbc.Alert(
            html.Div([
                html.Span(
                    "CACP is in PREVIEW mode, some actions are locked. "
                    "To enable them, run an instance on your machine "),
                html.A("https://cacp.readthedocs.io/", href="https://cacp.readthedocs.io/", target="_blank")
            ]),
            color="info",
            dismissable=True,
            is_open=True,
            style={
                "position": "fixed",
                "top": 20,
                "left": 0,
                "right": 0,
                "width": "50%",
                "margin": "0 auto"
            }
        ) if is_preview() else "",
    ])
    app.logger.setLevel(log_level)

    print(f"CACP stared on http://{host}:{port}/")
    app.run_server(debug=debug, host=host, port=port)


if __name__ == "__main__":
    start()
