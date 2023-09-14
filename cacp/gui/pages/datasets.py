import dash
from dash import html, Input, callback, no_update

from cacp.gui.components.datasets.custom_datasets_table import CustomDatasetsTable
from cacp.gui.components.datasets.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.datasets.river_datasets_table import RiverDatasetsTable
from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_datasets import add_custom_dataset
from cacp.gui.preview import preview_button_kwargs

dash.register_page(__name__)

ADD_CUSTOM_DATASET_BUTTON_ID = "add_custom_dataset_button"

layout = html.Div([
    html.Div(html.Button("Add custom dataset", className="btn btn-primary", id=ADD_CUSTOM_DATASET_BUTTON_ID,
                         **preview_button_kwargs()),
             className="d-flex justify-content-end mb-4"),
    html.H5("Custom datasets"),
    CustomDatasetsTable("cdt"),
    html.H5("Keel datasets (BATCH, INCREMENTAL)", className="mt-4"),
    KeelDatasetsTable("kdt"),
    html.H5("River datasets (INCREMENTAL)", className="mt-4"),
    RiverDatasetsTable("rdt"),
])


@callback(
    global_location_href_output(),
    Input(ADD_CUSTOM_DATASET_BUTTON_ID, "n_clicks"),
    prevent_initial_call=True,
)
def add_custom_dataset_button(n_clicks):
    if n_clicks:
        custom_dataset_id = add_custom_dataset()
        return f"/custom_dataset/{custom_dataset_id}"

    return no_update
