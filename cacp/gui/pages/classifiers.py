import dash
from dash import html

from cacp.gui.components.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.sklearn_classifiers_table import SklearnClassifiersTable

dash.register_page(__name__)

layout = html.Div([
    SklearnClassifiersTable(),
    html.Br(),
    RiverClassifiersTable(),
])
