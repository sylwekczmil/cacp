from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from PIL import Image
from dash import html, Output, Input, no_update, callback, dcc
from dash.dcc import Store

from cacp.gui.components.experiments.details.processor import ExperimentProcessor
from cacp.gui.components.shared.utils import csv_to_grid
from cacp.gui.db.experiments import get_experiment, Experiment, ExperimentStatus, ExperimentType
from cacp.gui.preview import is_preview

dash.register_page(__name__, path_template="/experiment/<experiment_id>")

EXPERIMENT_STORE_ID = "experiment_store"
EXPERIMENT_RESULTS_ID = "experiment_results"
EXPERIMENT_RESULTS_PATH_ID = "experiment_results_path"


def show_experiment(experiment: Experiment):
    experiment_path = Path(experiment["path"])

    incremental_components = html.Div([])
    if experiment["type"] == ExperimentType.INCREMENTAL:
        incremental_components = html.Div([
            html.H5("Incremental plots", className="mt-4"),
            html.Div([
                html.Div([
                    html.P(plot.name.split("_")[0].upper() + " dataset", className="image-title"),
                    html.Div(html.Img(src=Image.open(plot)), className="d-flex justify-content-center"),
                ], className="col mt-5 position-relative") for plot in
                experiment_path.joinpath("incremental").joinpath("plot").glob("*.png")
            ], className="row justify-content-md-center")
        ])

    return html.Div([
        html.H5("Directory", className="mt-4"),
        dbc.InputGroup([
            dbc.Input(
                id=EXPERIMENT_RESULTS_PATH_ID,
                value=experiment["path"],
                readonly=True
            ),
            dcc.Clipboard(
                target_id=EXPERIMENT_RESULTS_PATH_ID,
                title="copy",
                style={
                    "margin-left": 10,
                    "fontSize": 25,
                },
            ),
        ]),
        html.H5("Datasets", className="mt-4"),
        csv_to_grid(experiment_path / "info" / "datasets.csv", skip_first_column=True),
        html.H5("Classifiers", className="mt-4"),
        csv_to_grid(experiment_path / "info" / "classifiers.csv", skip_first_column=True),
        html.H5("Comparison results", className="mt-4"),
        csv_to_grid(experiment_path / "comparison_result.csv", skip_first_column=True),
        html.H5("Comparison results winner", className="mt-4"),
        csv_to_grid(experiment_path / "winner" / "comparison.csv", skip_first_column=True),
        html.H5("Comparison times", className="mt-4"),
        csv_to_grid(experiment_path / "time" / "comparison.csv"),
        html.H5("Wilcoxon results", className="mt-4"),
        html.Div([
            html.Div([
                html.P(csv.name.split("_")[1].split(".")[0] + " vs:"),
                csv_to_grid(csv, True),
                html.Br(),
                html.Br()
            ]) for csv in experiment_path.joinpath("wilcoxon").glob("comparison_*.csv")
        ]),
        html.H5("Result plots", className="mt-4"),
        html.Div([
            html.Div([
                html.Img(src=Image.open(plot)),
                html.Br(),
                html.Br()
            ], className="col mt-5") for plot in experiment_path.joinpath("plot").glob("comparison_*_per_fold.png")
        ], className="row justify-content-md-center"),
        incremental_components
    ])


EXPERIMENT_PROCESSOR = ExperimentProcessor(EXPERIMENT_STORE_ID)


def layout(experiment_id=None):
    experiment = get_experiment(experiment_id) if experiment_id else None
    view = html.Div([
        EXPERIMENT_PROCESSOR if experiment and experiment[
            "status"] == ExperimentStatus.RUNNING and not is_preview() else "",
        html.Div(show_experiment(experiment) if experiment else [], id=EXPERIMENT_RESULTS_ID),
        Store(id=EXPERIMENT_STORE_ID, data=experiment),
    ])
    return view


@callback(
    Output(EXPERIMENT_RESULTS_ID, "children"),
    Input(EXPERIMENT_STORE_ID, "data")
)
def on_experiment_changed(experiment: Experiment):
    if experiment:
        return show_experiment(experiment)
    return no_update
