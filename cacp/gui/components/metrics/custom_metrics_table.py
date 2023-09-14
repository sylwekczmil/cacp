import dash_ag_grid as dag
from dash import html, Output, Input, no_update, callback, State
from dash.dcc import Store

from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_metrics import get_all_custom_metrics, delete_custom_metric
from cacp.gui.preview import preview_button_kwargs


class CustomMetricsTable(html.Div):
    class ids:
        table = lambda aio_id: f"CustomMetricsTable-table-{aio_id}"
        store = lambda aio_id: f"CustomMetricsTable-store-{aio_id}"

    ids = ids

    @property
    def data(self):
        return get_all_custom_metrics()

    def __init__(
        self,
        aio_id,
        store_id=None
    ):
        self.table_id = self.ids.table(aio_id)
        self.store_id = store_id
        if store_id is None:
            self.store_id = self.ids.store(aio_id)

        super().__init__([
            dag.AgGrid(
                id=self.table_id,
                rowData=self.data,
                columnDefs=[
                    {"field": "id", "headerName": "#", "maxWidth": 100, "checkboxSelection": bool(store_id)},
                    {"field": "name", "maxWidth": None},
                    {"field": "type"},
                    {"field": "created at", "maxWidth": 200},
                    {
                        "field": "remove", "headerName": "", "maxWidth": 120, "sortable": False, "filter": False,
                        "resizable": False,
                        "cellRenderer": "Button",
                        "cellRendererParams": {
                            "buttonName": "Delete",
                            "buttonClassName": "btn btn-sm btn-danger",
                            "iconClassName": "bi bi-trash delete-button",
                            **preview_button_kwargs()
                        },
                    },
                    {
                        "field": "navigate", "headerName": "", "maxWidth": 120, "sortable": False, "filter": False,
                        "resizable": False,
                        "cellRenderer": "Button",
                        "cellRendererParams": {
                            "buttonName": "Open",
                            "buttonClassName": "btn btn-sm btn-primary",
                            "iconClassName": "bi bi-forward-fill"
                        },
                    },
                ],
                defaultColDef={"sortable": True, "filter": True, "resizable": True},
                dashGridOptions={"rowSelection": "single"} if store_id else None,
                columnSize="responsiveSizeToFit",
            ),
            Store(id=self.store_id)
        ])

        if store_id:
            @callback(
                Output(store_id, "data"),
                Input(self.table_id, "selectedRows"),
            )
            def selection_change(selected):
                return selected

        @callback(
            global_location_href_output(),
            Output(self.table_id, "rowData"),
            Input(self.table_id, "cellRendererData"),
            State(self.table_id, "rowData"),
            config_prevent_initial_callbacks="initial_duplicate"  # this will refresh every page reload
        )
        def on_metrics_renderer_data(
            custom_metrics_renderer_data,
            custom_metrics
        ):
            if custom_metrics_renderer_data:
                idx = custom_metrics_renderer_data["rowIndex"]
                custom_metric_id = custom_metrics[idx]["id"]

                if custom_metrics_renderer_data["colId"] == "navigate":
                    return f"/custom_metric/{custom_metric_id}", no_update

                if custom_metrics_renderer_data["colId"] == "remove":
                    delete_custom_metric(custom_metric_id)

            return no_update, get_all_custom_metrics()
