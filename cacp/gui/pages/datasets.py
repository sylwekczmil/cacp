import dash
from dash import html, Input, callback, no_update

from cacp.gui.components.datasets.custom_datasets_table import CustomDatasetsTable
from cacp.gui.components.datasets.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.datasets.river_datasets_table import RiverDatasetsTable
from cacp.gui.components.shared.utils import global_location_href_output

dash.register_page(__name__)

ADD_CUSTOM_DATASET_BUTTON_ID = "add_custom_dataset_button"

custom_datasets_table = CustomDatasetsTable("cdt")

layout = html.Div([
    html.Div(html.Button("Add custom dataset", className="btn btn-primary", id=ADD_CUSTOM_DATASET_BUTTON_ID),
             className="d-flex justify-content-end mb-4"),
    html.H5("Custom datasets"),
    custom_datasets_table,
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
    href = no_update
    if n_clicks:
        # TODO:
        # custom_dataset_id = add_custom_dataset()
        # custom_datasets_table = get_all_custom_datasets()
        # href = f"/custom_dataset/{custom_dataset_id}"
        pass

    return href
