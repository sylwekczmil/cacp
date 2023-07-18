import traceback

import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, no_update

from cacp import run_experiment, run_incremental_experiment
from cacp.gui.components.shared.utils import GLOBAL_LOCATION_ID
from cacp.gui.db.experiments import get_experiment, ExperimentStatus, ExperimentType, update_experiment_status
from cacp.gui.external.classifier import process_classifiers_names, parse_classifier
from cacp.gui.external.dataset import parse_dataset


def make_progress_graph(progress: int, total: int):
    if total == 0:
        return dbc.Progress(label="Loading", value=100, className="mt-4 mb-4", animated=True, striped=True)

    value = int(progress / (total + 1) * 100)
    return html.Div([
        html.P("Experiment is running, do not close this page", className="lead"),
        dbc.Progress(label=f"{value}%", value=value, className="mt-4 mb-4", animated=True, striped=True),
    ])


class ExperimentProcessor(html.Div):

    def __init__(
        self,
        experiment_store_id
    ):

        self.experiment_processor_progres_id = "experiment_processor_progres"
        super().__init__([
            html.Div(make_progress_graph(0, 0), id=self.experiment_processor_progres_id)
        ])

        # TODO: cancell job on page change
        @callback(
            Output(experiment_store_id, "data"),
            Input(GLOBAL_LOCATION_ID, "pathname"),
            prevent_initial_call=False,
            background=True,
            running=[
                (Output(self.experiment_processor_progres_id, "children"), make_progress_graph(0, 0), []),
            ],
            progress=Output(self.experiment_processor_progres_id, "children"),
        )
        def on_page_load(set_progress, pathname: str):
            result = no_update
            path_split = pathname.split("/")
            if len(path_split) > 2:
                experiment_id = int(path_split[2])
                experiment = get_experiment(experiment_id)
                if experiment and experiment["status"] == ExperimentStatus.RUNNING:
                    try:
                        def progress(p: int, t: int):
                            set_progress(make_progress_graph(p, t))

                        classifier_names = process_classifiers_names(
                            [c["name"] for c in experiment["classifiers"]]
                        )
                        experiment_type = experiment["type"]
                        if experiment_type == ExperimentType.BATCH:
                            update_experiment_status(experiment_id, ExperimentStatus.RUNNING)
                            run_experiment(
                                [parse_dataset(d) for d in experiment["datasets"]],
                                list(zip(classifier_names, [parse_classifier(c) for c in experiment["classifiers"]])),
                                experiment["path"],
                                progress=progress,
                            )
                        elif experiment_type == ExperimentType.INCREMENTAL:
                            update_experiment_status(experiment_id, ExperimentStatus.RUNNING)
                            run_incremental_experiment(
                                [parse_dataset(d) for d in experiment["datasets"]],
                                list(zip(classifier_names, [parse_classifier(c) for c in experiment["classifiers"]])),
                                experiment["path"],
                                progress=progress,
                            )
                        update_experiment_status(experiment_id, ExperimentStatus.FINISHED)
                    except Exception as e:
                        print(e, traceback.format_exc())
                        update_experiment_status(experiment_id, ExperimentStatus.FAILED)

                    result = get_experiment(experiment_id)

            return result
