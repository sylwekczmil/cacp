import uuid

import dash_ag_grid as dag
from dash import html

from cacp.gui.external.classifier import SKLEARN_CLASSIFIERS


class SklearnClassifiersTable(html.Div):
    class ids:
        table = lambda aio_id: {
            'component': 'SklearnClassifiersTable',
            'subcomponent': 'table',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        aio_id=None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__([
            html.H3("Sklearn classifiers (batch)"),
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=SKLEARN_CLASSIFIERS,
                columnDefs=[
                    {'field': '#', "headerName": "#", "maxWidth": 100},
                    {'field': 'name', "headerName": "Name"},
                    {'field': 'docs_url', "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {'field': 'id', "cellRenderer": "markdown", "headerName": "Python path", "maxWidth": None},
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True},
                columnSize="responsiveSizeToFit",
            )
        ])
