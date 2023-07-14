import dash_ag_grid as dag
from dash import html, callback, Input, Output
from dash.dcc import Store


class CustomDatasetsTable(html.Div):
    class ids:
        table = lambda aio_id: f"CustomDatasetsTable-table-{aio_id}"
        store_id = lambda aio_id: f"CustomDatasetsTable-store_id-{aio_id}"

    ids = ids

    @property
    def data(self):
        return [
        ]

    def __init__(
        self,
        aio_id,
        store_id=None
    ):

        self.store_id = store_id
        if store_id is None:
            self.store_id = self.ids.store_id(aio_id)

        super().__init__([
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=self.data,
                columnDefs=[
                    {"field": "#", "headerName": "#", "maxWidth": 100, "checkboxSelection": bool(store_id)},
                    {"field": "Name", "headerName": "Name"},
                    {"field": "Instances"},
                    {"field": "Features"},
                    {"field": "Classes"},
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True, "resizable": True},
                dashGridOptions={"rowSelection": "single"} if store_id else None,
                columnSize="responsiveSizeToFit",
            ),
            Store(id=self.store_id)
        ])

        if store_id:
            @callback(
                Output(store_id, "data"),
                Input(self.ids.table(aio_id), "selectedRows"),
            )
            def selection_change(selected):
                return selected
