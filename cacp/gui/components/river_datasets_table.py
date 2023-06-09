import uuid

import dash_ag_grid as dag
from dash import html

from cacp.gui.external.river_library.dataset import RiverDatasetModel


class RiverDatasetsTable(html.Div):
    class ids:
        table = lambda aio_id: {
            'component': 'RiverDatasetsTable',
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

        valid_datasets = sorted([rd for rd in RiverDatasetModel.all() if rd.classes > 0 and rd.samples > 0],
                                key=lambda x: x.name)

        super().__init__([
            html.H3("River datasets (incremental)"),
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=[
                    {"#": i + 1, **frd.dict(), "docs_url": f"[{frd.docs_url}]({frd.docs_url})"} for i, frd
                    in enumerate(valid_datasets)
                ],
                columnDefs=[
                    {'field': '#', "headerName": "#", "maxWidth": 100},
                    {'field': 'name', "headerName": "Name"},
                    {'field': 'docs_url', "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {'field': 'samples', "headerName": "Instances", "filter": "agNumberColumnFilter"},
                    {'field': 'features', "headerName": "Features", "filter": "agNumberColumnFilter"},
                    {'field': 'classes', "headerName": "Classes", "filter": "agNumberColumnFilter"},
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True},
                columnSize="responsiveSizeToFit",
            )
        ])
