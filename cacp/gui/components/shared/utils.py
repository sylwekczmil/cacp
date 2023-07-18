from pathlib import Path

import dash_ag_grid as dag
import pandas as pd
from dash import Output


def csv_to_grid(path: Path, skip_first_column=False):
    columns = []
    row_data = []

    if path.exists():
        df = pd.read_csv(path)
        columns = df.columns
        if skip_first_column:
            columns = columns[1:]
        row_data = df[columns].to_dict("records")

    return dag.AgGrid(
        rowData=row_data,
        columnDefs=[
            {"field": c} for c in columns
        ],
        defaultColDef={"sortable": True, "filter": True, "resizable": True},
        columnSize="responsiveSizeToFit",
    )


def global_location_href_output():
    return Output(GLOBAL_LOCATION_ID, "href", allow_duplicate=True)


GLOBAL_LOCATION_ID = "global_location"
