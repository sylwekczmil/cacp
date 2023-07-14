import dash
from dash import html

from cacp.gui.components.datasets.custom_datasets_table import CustomDatasetsTable
from cacp.gui.components.datasets.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.datasets.river_datasets_table import RiverDatasetsTable

dash.register_page(__name__)

layout = html.Div([
    html.H5("Custom datasets (batch, incremental)"),
    CustomDatasetsTable("cdt"),
    html.H5("Keel datasets (batch, incremental)", className="mt-4"),
    KeelDatasetsTable("kdt"),
    html.H5("River datasets (incremental)", className="mt-4"),
    RiverDatasetsTable("rdt"),
])
