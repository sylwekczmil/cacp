import dash
from dash import html

from cacp.gui.components.classifiers.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.classifiers.sklearn_classifiers_table import SklearnClassifiersTable

dash.register_page(__name__)

layout = html.Div([
    html.H5("Sklearn classifiers (batch)"),
    SklearnClassifiersTable(),
    html.Br(),
    html.H5("River classifiers (incremental)"),
    RiverClassifiersTable(),
])
