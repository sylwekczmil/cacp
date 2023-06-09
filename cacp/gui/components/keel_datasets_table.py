import uuid

import dash_ag_grid as dag
import pandas as pd
from dash import html

from cacp.gui.assets import ASSETS_PATH


class KeelDatasetsTable(html.Div):
    class ids:
        table = lambda aio_id: {
            'component': 'KeelDatasetsTable',
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
            html.H3("Keel datasets (batch, incremental)"),
            dag.AgGrid(
                id=self.ids.table(aio_id),
                rowData=[
                    {**r, "docs_url": f"[{r['docs_url']}]({r['docs_url']})"} for r in [
                        {**r,
                         "docs_url": f"https://sci2s.ugr.es/keel/dataset/data/classification/{r['Name']}-names.txt"
                         } for r in pd.read_csv(ASSETS_PATH.joinpath("datasets.csv")).to_dict("records")
                    ]
                ],
                columnDefs=[
                    {'field': '#', "headerName": "#", "maxWidth": 100},
                    {'field': 'Name', "headerName": "Name"},
                    {'field': 'docs_url', "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {'field': 'Instances'},
                    {'field': 'Features'},
                    {'field': 'Classes'},
                ],
                defaultColDef={"maxWidth": 160, "sortable": True, "filter": True},
                columnSize="responsiveSizeToFit",
            )
        ])
