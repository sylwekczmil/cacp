import shutil
from datetime import datetime
from enum import Enum
from typing import TypedDict, List, Dict, Optional

from tinydb import TinyDB
from tinydb.table import Document

from cacp.gui.custom import CUSTOM_DIR
from cacp.gui.db import DB_PATH


class ExperimentType(str, Enum):
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"


class ExperimentStatus(str, Enum):
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class Experiment(TypedDict):
    id: int
    path: Optional[str]
    name: str
    datasets: List[Dict]
    classifiers: List[Dict]
    metrics: List[Dict]
    type: ExperimentType
    status: ExperimentStatus
    created_at: float


EXPERIMENTS_DB = TinyDB(CUSTOM_DIR / "experiments.json")
EXPERIMENTS_PATH = (DB_PATH / "experiments").resolve()


def _convert_from_document_to_experiment(experiment: Document) -> Experiment:
    experiment["id"] = experiment.doc_id
    experiment["number of datasets"] = len(experiment["datasets"])
    experiment["number of classifiers"] = len(experiment["classifiers"])
    experiment["created at"] = datetime.fromtimestamp(experiment["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
    return experiment


def get_all_experiments() -> List[Experiment]:
    return [_convert_from_document_to_experiment(e) for e in EXPERIMENTS_DB.all()]


def get_experiment(experiment_id: int) -> Experiment:
    return _convert_from_document_to_experiment(EXPERIMENTS_DB.get(doc_id=experiment_id))


def add_experiment(
    name_value: str, type_value: ExperimentType, selected_datasets: List[Dict], selected_classifiers: List[Dict],
    selected_metrics: List[Dict]
) -> int:
    new_experiment: Experiment = dict()
    new_experiment["name"] = name_value
    new_experiment["type"] = type_value
    new_experiment["datasets"] = selected_datasets
    new_experiment["classifiers"] = selected_classifiers
    new_experiment["metrics"] = selected_metrics
    new_experiment["status"] = ExperimentStatus.RUNNING
    new_experiment["created_at"] = datetime.now().timestamp()
    experiment_id = EXPERIMENTS_DB.insert(new_experiment)
    EXPERIMENTS_DB.update({"path": str((EXPERIMENTS_PATH / str(experiment_id)).as_posix())}, doc_ids=[experiment_id])
    return experiment_id


def update_experiment_status(experiment_id: int, experiment_status: ExperimentStatus):
    EXPERIMENTS_DB.update({"status": experiment_status}, doc_ids=[experiment_id])


def delete_experiment(experiment_id: int):
    experiment = get_experiment(experiment_id)
    shutil.rmtree(experiment["path"], ignore_errors=True)
    EXPERIMENTS_DB.remove(doc_ids=[experiment_id])
