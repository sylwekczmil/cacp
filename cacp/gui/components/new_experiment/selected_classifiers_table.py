import uuid

import dash_ag_grid as dag
from dash import html, callback, Output, Input
from dash.dcc import Store


class SelectedClassifiersTable(html.Div):
    class ids:
        table = lambda aio_id: {
            'component': 'SelectedClassifiersTable',
            'subcomponent': 'table',
            'aio_id': aio_id
        }
        output = lambda aio_id: {
            'component': 'SelectedClassifiersTable',
            'subcomponent': 'output',
            'aio_id': aio_id
        }
        store_id = lambda aio_id: {
            'component': 'SelectedClassifiersTable',
            'subcomponent': 'store_id',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        store_id,
        aio_id=None
    ):
        self.aio_id = aio_id
        if self.aio_id is None:
            self.aio_id = str(uuid.uuid4())

        super().__init__([
            dag.AgGrid(
                id=self.ids.table(self.aio_id),
                rowData=[],
                columnDefs=[
                    {'field': 'name', "headerName": "Name"},
                    {'field': 'docs_url', "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {'field': 'id', "cellRenderer": "markdown", "headerName": "Python path", "maxWidth": None},
                    {'field': 'id', "cellRenderer": "Button", "cellRendererParams": {}, },
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True},
                columnSize="responsiveSizeToFit",
            ),
            Store(id=store_id)
        ])

        @callback(
            Output(self.ids.table(self.aio_id), 'rowData'),
            Input(store_id, "data"),

        )
        def selection_change(selected):
            return selected
