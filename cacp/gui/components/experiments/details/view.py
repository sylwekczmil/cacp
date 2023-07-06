import uuid
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input
from dash.dcc import Store

from cacp.gui.components.experiments.details.process import process_experiment
from cacp.gui.components.shared.utils import csv_to_grid
from cacp.gui.db.experiments import get_experiment


class ExperimentDetails(html.Div):
    class ids:
        store = lambda aio_id: f"ExperimentDetails-store-{aio_id}"
        alert = lambda aio_id: f"ExperimentDetails-alert-{aio_id}"
        results = lambda aio_id: f"ExperimentDetails-alert-{aio_id}"

    ids = ids

    def __init__(
        self,
        aio_id
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        super().__init__([
            html.Div([], id=self.ids.alert(aio_id)),
            html.Div([], id=self.ids.results(aio_id)),
            Store(id=self.ids.store(aio_id), data=None)
        ])

        @callback(
            Output(self.ids.store(aio_id), "data"),
            Input("location", "pathname"),
            prevent_initial_call=False,
            background=True,
            running=[
                (Output(self.ids.alert(aio_id), "children"), dbc.Alert(
                    "Running..."
                ), ""),
            ],
        )
        def on_page_load(pathname: str):
            experiment_id = int(pathname.split("/")[2])
            process_experiment(experiment_id)
            return get_experiment(experiment_id)

        @callback(
            Output(self.ids.results(aio_id), "children"),
            Input(self.ids.store(aio_id), "data")
        )
        def on_experiment_loaded(experiment: dict):
            if experiment:
                experiment_path = Path(experiment["path"])
                return html.Div([
                    html.H5("Comparison results"),
                    csv_to_grid(experiment_path / "comparison_result.csv", skip_first_column=True),
                    html.Br(),
                    html.H5("Comparison results winner"),
                    csv_to_grid(experiment_path / "winner" / "comparison.csv", skip_first_column=True),
                    html.Br(),
                    html.H5("Comparison times"),
                    csv_to_grid(experiment_path / "time" / "comparison.csv"),
                    html.Br(),
                ])
            return "Error..."
