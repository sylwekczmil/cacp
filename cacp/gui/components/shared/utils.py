from pathlib import Path

import dash_ag_grid as dag
import pandas as pd
from dash import Output


def csv_to_grid(path: Path, skip_first_column=False):
    df = pd.read_csv(path)
    columns = df.columns
    if skip_first_column:
        columns = columns[1:]
    return dag.AgGrid(
        rowData=df[columns].to_dict("records"),
        columnDefs=[
            {"field": c} for c in columns
        ],
        defaultColDef={"sortable": True, "filter": True, "resizable": True},
        columnSize="responsiveSizeToFit",
    )


def location_href_output():
    return Output("location", "href", allow_duplicate=True)
