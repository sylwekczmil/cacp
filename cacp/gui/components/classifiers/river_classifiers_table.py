import uuid

import dash_ag_grid as dag
from dash import html, callback, Output, Input
from dash.dcc import Store

from cacp.gui.external.classifier import RIVER_CLASSIFIERS


class RiverClassifiersTable(html.Div):
    class ids:
        table = lambda aio_id: {
            'component': 'RiverClassifiersTable',
            'subcomponent': 'table',
            'aio_id': aio_id
        }
        store_id = lambda aio_id: {
            'component': 'RiverClassifiersTable',
            'subcomponent': 'store_id',
            'aio_id': aio_id
        }

    ids = ids

    @property
    def data(self):
        return RIVER_CLASSIFIERS

    def __init__(
        self,
        store_id=None,
        aio_id=None
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self.store_id = store_id
        if store_id is None:
            self.store_id = self.ids.store_id(aio_id)

        super().__init__([
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=self.data,
                columnDefs=[
                    {'field': '#', "headerName": "#", "maxWidth": 100, "checkboxSelection": bool(store_id)},
                    {'field': 'name', "headerName": "Name"},
                    {'field': 'docs_url', "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {'field': 'id', "cellRenderer": "markdown", "headerName": "Python path", "maxWidth": None},
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True},
                dashGridOptions={"rowSelection": "single"} if store_id else None,
                columnSize="responsiveSizeToFit",
            ),
            Store(id=self.store_id)
        ])

        @callback(
            Output(self.store_id, "data"),
            Input(self.ids.table(aio_id), 'selectedRows'),
        )
        def selection_change(selected):
            return selected