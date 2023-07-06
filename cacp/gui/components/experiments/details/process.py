import traceback

from cacp import run_experiment, run_incremental_experiment
from cacp.gui.db.experiments import get_experiment, ExperimentStatus, ExperimentType, update_experiment_status
from cacp.gui.external.classifier import process_classifiers_names, parse_classifier
from cacp.gui.external.dataset import parse_dataset


def process_experiment(experiment_id: int):
    experiment = get_experiment(experiment_id)
    if experiment["status"] == ExperimentStatus.RUNNING:
        # TODO: https://dash.plotly.com/background-callbacks#example-5:-progress-bar-chart-graph
        try:
            classifier_names = process_classifiers_names(
                [c["name"] for c in experiment["classifiers"]]
            )
            experiment_type = experiment["type"]
            if experiment_type == ExperimentType.BATCH:
                run_experiment(
                    [parse_dataset(d) for d in experiment["datasets"]],
                    list(zip(classifier_names, [parse_classifier(c) for c in experiment["classifiers"]])),
                    experiment["path"]
                )
            elif experiment_type == ExperimentType.INCREMENTAL:
                run_incremental_experiment(
                    [parse_dataset(d) for d in experiment["datasets"]],
                    list(zip(classifier_names, [parse_classifier(c) for c in experiment["classifiers"]])),
                    experiment["path"]
                )
            update_experiment_status(experiment_id, ExperimentStatus.FINISHED)
        except:
            print(traceback.format_exc())
            update_experiment_status(experiment_id, ExperimentStatus.FAILED)
