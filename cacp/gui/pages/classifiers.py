import dash
from dash import html

from cacp.gui.components.classifiers.custom_classifiers_table import CustomClassifiersTable
from cacp.gui.components.classifiers.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.classifiers.sklearn_classifiers_table import SklearnClassifiersTable

dash.register_page(__name__)

layout = html.Div([
    html.H5("Custom classifiers (batch, incremental)"),
    CustomClassifiersTable("cct"),
    html.H5("Sklearn classifiers (batch)", className="mt-4"),
    SklearnClassifiersTable("sct"),
    html.H5("River classifiers (incremental)", className="mt-4"),
    RiverClassifiersTable("rct"),
])
