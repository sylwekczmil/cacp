import tempfile
import traceback
import typing
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TypedDict, List

from river import metrics as river_metrics
from river.dummy import NoChangeClassifier
from sklearn.dummy import DummyClassifier
from tinydb import TinyDB
from tinydb.table import Document

from cacp import ClassificationDataset
from cacp.comparison import process_comparison_single, process_incremental_comparison_single
from cacp.gui.custom.metrics import CUSTOM_METRICS_CODE_DIR
from cacp.gui.external.metric import parse_metric
from cacp.gui.preview import preview_prevent_modifications
from cacp.util import accuracy


class CustomMetricType(str, Enum):
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"


class CustomMetric(TypedDict):
    id: int
    locate_id: str
    name: str
    type: CustomMetricType
    code: str
    created_at: float


CUSTOM_METRICS_DB = TinyDB(CUSTOM_METRICS_CODE_DIR / "metrics.json")
CUSTOM_METRIC_BATCH_CODE_TEMPLATE = """import numpy as np


def metric{}(y_true: np.ndarray, y_pred: np.ndarray, labels: np.ndarray):  # do not change function declaration
    return 0.5
"""

CUSTOM_INCREMENTAL_METRIC_CODE_TEMPLATE = """from river.metrics.base import ClassificationMetric


class Metric{}(ClassificationMetric):  # do not change class declaration
    def get(self) -> float:
        return 0.5
"""


def _convert_from_document_to_custom_metric(custom_metric: Document) -> CustomMetric:
    if custom_metric:
        custom_metric["id"] = custom_metric.doc_id
        custom_metric["created at"] = datetime.fromtimestamp(custom_metric["created_at"]).strftime(
            "%Y-%m-%d %H:%M:%S")
        custom_metric["json_schema"] = {
            "title": custom_metric["name"],
            "type": "object",
            "properties": {
            }
        }
    return custom_metric


def _locate_id(custom_metric_id: int, type_value: CustomMetricType,
               original_custom_metric_id: typing.Optional[int] = None):
    if original_custom_metric_id is None:
        original_custom_metric_id = custom_metric_id

    if type_value == CustomMetricType.BATCH:
        return f"cacp.gui.custom.metrics.metric{custom_metric_id}.metric{original_custom_metric_id}"
    else:
        return f"cacp.gui.custom.metrics.metric{custom_metric_id}.Metric{original_custom_metric_id}"


def _code_path(custom_metric_id: int) -> Path:
    return CUSTOM_METRICS_CODE_DIR.joinpath(f"metric{custom_metric_id}.py")


def _save_code(custom_metric_id: int, code: str):
    with _code_path(custom_metric_id).open("w") as f:
        f.write(code)


def _remove_code(custom_metric_id: int):
    _code_path(custom_metric_id).unlink(missing_ok=True)


def get_all_custom_metrics() -> List[CustomMetric]:
    return [_convert_from_document_to_custom_metric(e) for e in CUSTOM_METRICS_DB.all() if e is not None]


def get_custom_metric(custom_metric_id: int) -> CustomMetric:
    return _convert_from_document_to_custom_metric(CUSTOM_METRICS_DB.get(doc_id=custom_metric_id))


def add_custom_metric() -> int:
    preview_prevent_modifications()
    new_custom_metric: CustomMetric = dict()
    all_metrics = CUSTOM_METRICS_DB.all()
    new_custom_metric_id = 1 if len(all_metrics) == 0 else all_metrics[-1].doc_id + 1
    new_custom_metric["name"] = f"Custom Metric {new_custom_metric_id}"
    new_custom_metric["type"] = CustomMetricType.BATCH
    new_custom_metric["code"] = CUSTOM_METRIC_BATCH_CODE_TEMPLATE.format(new_custom_metric_id)
    new_custom_metric["locate_id"] = _locate_id(new_custom_metric_id, CustomMetricType.BATCH)
    new_custom_metric["created_at"] = datetime.now().timestamp()
    _save_code(new_custom_metric_id, new_custom_metric["code"])
    return CUSTOM_METRICS_DB.insert(new_custom_metric)


def update_custom_metric(
    custom_metric_id: int,
    name_value: str,
    type_value: CustomMetricType,
    code_value: str
):
    preview_prevent_modifications()
    CUSTOM_METRICS_DB.update({"name": name_value, "type": type_value, "code": code_value,
                              "locate_id": _locate_id(custom_metric_id, type_value)},
                             doc_ids=[custom_metric_id])
    _save_code(custom_metric_id, code_value)


def test_custom_metric_code(custom_metric_id: int, code_value: str, type_value: CustomMetricType):
    preview_prevent_modifications()
    error = None
    _save_code(0, code_value)
    metric_factory = parse_metric({"locate_id": _locate_id(0, type_value, custom_metric_id), "code": code_value})

    try:
        ds = ClassificationDataset("iris")
        ds_fold = next(ds.folds())
        if type_value == CustomMetricType.BATCH:
            process_comparison_single(lambda n_inputs, n_classes: DummyClassifier(), "test", ds, ds_fold,
                                      (('Accuracy', accuracy), ("Custom", metric_factory)))
        elif type_value == CustomMetricType.INCREMENTAL:
            with tempfile.TemporaryDirectory() as tmpdirname:
                process_incremental_comparison_single(
                    lambda n_inputs, n_classes: NoChangeClassifier(), "test",
                    ds, 3, Path(tmpdirname),
                    (('Accuracy', river_metrics.Accuracy), ("Custom", metric_factory))
                )
    except:
        error = traceback.format_exc()

    _remove_code(0)
    return error


def delete_custom_metric(custom_metric_id: int):
    preview_prevent_modifications()
    CUSTOM_METRICS_DB.remove(doc_ids=[custom_metric_id])
    _remove_code(custom_metric_id)
