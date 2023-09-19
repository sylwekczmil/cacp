import dash_ag_grid as dag
import pandas as pd
from dash import html, callback, Input, Output
from dash.dcc import Store

from cacp import ClassificationDataset
from cacp.gui.assets import ASSETS_PATH
from cacp.gui.external.shared.type import to_id


class KeelDatasetsTable(html.Div):
    class ids:
        table = lambda aio_id: f"KeelDatasetsTable-table-{aio_id}"
        store = lambda aio_id: f"KeelDatasetsTable-store-{aio_id}"

    ids = ids

    @property
    def data(self):
        return [
            {**r, "docs_url": f"[{r['docs_url']}]({r['docs_url']})"} for r in [
                {**r,
                 "docs_url": f"https://sci2s.ugr.es/keel/dataset/data/classification/{r['Name']}-names.txt",
                 "json_schema": {
                     "title": r["Name"],
                     "type": "object",
                     "properties": {
                     }
                 },
                 "id": to_id(ClassificationDataset)
                 } for r in pd.read_csv(ASSETS_PATH.joinpath("datasets.csv")).to_dict("records")
            ]
        ]

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
                    {"field": "Name", "headerName": "Name"},
                    {"field": "docs_url", "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
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
