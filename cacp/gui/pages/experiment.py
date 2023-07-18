from pathlib import Path

import dash
from dash import html, Output, Input, no_update, callback
from dash.dcc import Store

from cacp.gui.components.experiments.details.processor import ExperimentProcessor
from cacp.gui.components.shared.utils import csv_to_grid
from cacp.gui.db.experiments import get_experiment, Experiment

dash.register_page(__name__, path_template="/experiment/<experiment_id>")

EXPERIMENT_STORE_ID = "experiment_store"
EXPERIMENT_RESULTS_ID = "experiment_results"


def show_experiment(experiment: Experiment):
    experiment_path = Path(experiment["path"])
    return html.Div([
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
    ])


EXPERIMENT_PROCESSOR = ExperimentProcessor(EXPERIMENT_STORE_ID)


def layout(experiment_id=None):
    experiment = get_experiment(experiment_id) if experiment_id else None
    view = html.Div([
        EXPERIMENT_PROCESSOR,
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
