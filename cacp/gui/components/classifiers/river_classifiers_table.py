import dash_ag_grid as dag
from dash import html, callback, Output, Input
from dash.dcc import Store

from cacp.gui.external.classifier import RIVER_CLASSIFIERS


class RiverClassifiersTable(html.Div):
    class ids:
        table = lambda aio_id: f"RiverClassifiersTable-table-{aio_id}"
        store = lambda aio_id: f"RiverClassifiersTable-store-{aio_id}"

    ids = ids

    @property
    def data(self):
        return RIVER_CLASSIFIERS

    def __init__(
        self,
        aio_id,
        store_id=None
    ):

        self.store_id = store_id
        if store_id is None:
            self.store_id = self.ids.store(aio_id)

        super().__init__([
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=self.data,
                columnDefs=[
                    {"field": "#", "headerName": "#", "maxWidth": 100, "checkboxSelection": bool(store_id)},
                    {"field": "name", "headerName": "Name"},
                    {"field": "docs_url", "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {"field": "id", "cellRenderer": "markdown", "headerName": "Python path", "maxWidth": None},
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
