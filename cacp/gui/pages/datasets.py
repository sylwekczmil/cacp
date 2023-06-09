import dash
from dash import html

from cacp.gui.components.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.river_datasets_table import RiverDatasetsTable

dash.register_page(__name__)

layout = html.Div([
    KeelDatasetsTable(),
    html.Br(),
    RiverDatasetsTable(),
    html.Br(),
])
