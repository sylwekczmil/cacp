import dash_ag_grid as dag
from dash import html, callback, Output, Input
from dash.dcc import Store


class SelectedClassifiersTable(html.Div):
    class ids:
        table = lambda aio_id: f"SelectedClassifiersTable-table-{aio_id}"

    ids = ids

    def __init__(
        self,
        store_id,
        aio_id,
        init_data=None
    ):
        self.aio_id = aio_id

        if init_data is None:
            init_data = []

        super().__init__([
            dag.AgGrid(
                id=self.ids.table(self.aio_id),
                rowData=init_data,
                columnDefs=[
                    {"field": "name", "headerName": "Name"},
                    {"field": "docs_url", "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {"field": "id", "cellRenderer": "markdown", "headerName": "Python path", "maxWidth": None},
                    {
                        "field": "name", "headerName": "", "sortable": False, "filter": False, "resizable": False,
                        "cellRenderer": "Button",
                        "cellRendererParams": {
                            "buttonName": "Delete",
                            "buttonClassName": "btn btn-sm btn-danger",
                            "iconClassName": "bi bi-trash delete-button"
                        },
                    },
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True, "resizable": True},
                columnSize="responsiveSizeToFit",
            ),
            Store(id=store_id, data=init_data)
        ])

        @callback(
            Output(self.ids.table(self.aio_id), "rowData"),
            Input(store_id, "data"),

        )
        def selection_change(selected):
            return selected
