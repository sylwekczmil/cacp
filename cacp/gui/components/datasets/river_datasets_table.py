import dash_ag_grid as dag
from dash import html, callback, Output, Input
from dash.dcc import Store

from cacp.gui.external.river_library.dataset import RiverDatasetModel


class RiverDatasetsTable(html.Div):
    class ids:
        table = lambda aio_id: f"RiverDatasetsTable-table-{aio_id}"
        store_id = lambda aio_id: f"RiverDatasetsTable-store_id-{aio_id}"

    ids = ids

    @property
    def data(self):
        valid_datasets = sorted([rd for rd in RiverDatasetModel.all() if rd.classes > 0 and rd.samples > 0],
                                key=lambda x: x.name)
        return [
            {"#": i + 1, **frd.dict(), "docs_url": f"[{frd.docs_url}]({frd.docs_url})",
             "json_schema": frd.json_schema} for i, frd
            in enumerate(valid_datasets)
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
                    {"field": "name", "headerName": "Name"},
                    {"field": "docs_url", "cellRenderer": "markdown", "headerName": "Docs", "maxWidth": None},
                    {"field": "samples", "headerName": "Instances", "filter": "agNumberColumnFilter"},
                    {"field": "features", "headerName": "Features", "filter": "agNumberColumnFilter"},
                    {"field": "classes", "headerName": "Classes", "filter": "agNumberColumnFilter"},
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
