import dash
import dash_ag_grid as dag
from dash import html, callback, Output, Input, State, no_update

from cacp.gui.components.shared.utils import location_href_output
from cacp.gui.db.experiments import get_all_experiments, delete_experiment

dash.register_page(__name__, path="/")

experiments_table_id = "experiments_table"


def layout():
    init_experiments = get_all_experiments()

    view = html.Div([
        html.H5("Experiments"),
        dag.AgGrid(
            id=experiments_table_id,
            rowData=init_experiments,
            columnDefs=[
                {"field": "name"},
                {"field": "type"},
                {"field": "path", "maxWidth": None},
                {"field": "number of datasets"},
                {"field": "number of classifiers"},
                {"field": "status"},
                {"field": "created at"},
                {
                    "field": "remove", "headerName": "", "sortable": False, "filter": False, "resizable": False,
                    "maxWidth": 120,
                    "cellRenderer": "Button",
                    "cellRendererParams": {
                        "buttonName": "Delete",
                        "buttonClassName": "btn btn-sm btn-danger",
                        "iconClassName": "bi bi-trash delete-button"
                    },
                },
                {
                    "field": "navigate", "headerName": "", "sortable": False, "filter": False, "resizable": False,
                    "maxWidth": 110,
                    "cellRenderer": "Button",
                    "cellRendererParams": {
                        "buttonName": "Open",
                        "buttonClassName": "btn btn-sm btn-primary",
                        "iconClassName": "bi bi-forward-fill"
                    },
                },
            ],
            defaultColDef={"maxWidth": 200, "sortable": True, "filter": True, "resizable": True},
            columnSize="responsiveSizeToFit",
        ),
    ])
    return view


@callback(
    Output(experiments_table_id, "rowData"),
    location_href_output(),
    Input(experiments_table_id, "cellRendererData"),
    State(experiments_table_id, "rowData"),
    prevent_initial_call=True,
)
def on_experiments_renderer_data(
    experiments_renderer_data,
    experiments
):
    if not experiments_renderer_data:
        return no_update, no_update

    idx = experiments_renderer_data["rowIndex"]
    experiment_id = experiments[idx]["id"]

    if experiments_renderer_data["colId"] == "navigate":
        return no_update, f"/experiment/{experiment_id}"

    if experiments_renderer_data["colId"] == "remove":
        delete_experiment(experiment_id)

    return get_all_experiments(), no_update
