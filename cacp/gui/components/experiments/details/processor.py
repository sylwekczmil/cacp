import traceback

import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, no_update

from cacp import run_experiment, run_incremental_experiment
from cacp.gui.components.shared.utils import GLOBAL_LOCATION_ID
from cacp.gui.db.experiments import get_experiment, ExperimentStatus, ExperimentType, update_experiment_status
from cacp.gui.external.classifier import parse_classifier
from cacp.gui.external.dataset import parse_dataset
from cacp.gui.external.metric import parse_metric
from cacp.gui.external.shared.helpers import process_unique_names


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

        self.experiment_processor_progress_id = "experiment_processor_progress"
        super().__init__([
            html.Div(make_progress_graph(0, 0), id=self.experiment_processor_progress_id)
        ])

        @callback(
            Output(experiment_store_id, "data"),
            Input(GLOBAL_LOCATION_ID, "pathname"),
            prevent_initial_call=False,
            background=True,
            progress=Output(self.experiment_processor_progress_id, "children"),
            cancel=[Input(GLOBAL_LOCATION_ID, "href")],
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

                        classifier_names = process_unique_names(
                            [c["name"] for c in experiment["classifiers"]]
                        )
                        classifiers = list(
                            zip(classifier_names, [parse_classifier(c) for c in experiment["classifiers"]]))
                        datasets = [parse_dataset(d) for d in experiment["datasets"]]
                        metric_names = process_unique_names(
                            [m["name"] for m in experiment["metrics"]]
                        )
                        metrics = list(zip(metric_names, [parse_metric(m) for m in experiment["metrics"]]))
                        experiment_type = experiment["type"]
                        if experiment_type == ExperimentType.BATCH:
                            update_experiment_status(experiment_id, ExperimentStatus.RUNNING)
                            run_experiment(
                                datasets,
                                classifiers,
                                experiment["path"],
                                metrics,
                                progress=progress,
                            )
                        elif experiment_type == ExperimentType.INCREMENTAL:
                            update_experiment_status(experiment_id, ExperimentStatus.RUNNING)
                            run_incremental_experiment(
                                datasets,
                                classifiers,
                                experiment["path"],
                                metrics,
                                progress=progress,
                            )
                        update_experiment_status(experiment_id, ExperimentStatus.FINISHED)
                    except Exception as e:
                        print(e, traceback.format_exc())
                        update_experiment_status(experiment_id, ExperimentStatus.FAILED)

                    result = get_experiment(experiment_id)

            set_progress("")
            return result
