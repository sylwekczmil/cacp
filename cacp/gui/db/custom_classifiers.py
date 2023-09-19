import tempfile
import traceback
import typing
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TypedDict, List

from tinydb import TinyDB
from tinydb.table import Document

from cacp import ClassificationDataset
from cacp.comparison import process_comparison_single, DEFAULT_METRICS, process_incremental_comparison_single, \
    DEFAULT_INCREMENTAL_METRICS
from cacp.gui.custom.classifiers import CUSTOM_CLASSIFIERS_CODE_DIR
from cacp.gui.external.classifier import parse_classifier
from cacp.gui.preview import preview_prevent_modifications


class CustomClassifierType(str, Enum):
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"


class CustomClassifier(TypedDict):
    id: int
    locate_id: str
    name: str
    type: CustomClassifierType
    code: str
    created_at: float


CUSTOM_CLASSIFIERS_DB = TinyDB(CUSTOM_CLASSIFIERS_CODE_DIR / "classifiers.json")
CUSTOM_CLASSIFIER_BATCH_CODE_TEMPLATE = """import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


#  Example BATCH classifier, returns always first class
class Classifier{}(BaseEstimator, ClassifierMixin):  # do not change class declaration

    def __init__(self):
        self.class_value = None

    def fit(
            self,
            X: np.ndarray,  # 2d array
            y: np.ndarray  # 1d array
    ):
        self.class_value = y[0]
        return self

    def predict(
            self,
            X: np.ndarray  # 1d array
    ):
        if self.class_value is None:
            raise Exception("Classifier not fitted")

        return np.full(len(X), self.class_value)
"""

CUSTOM_INCREMENTAL_CLASSIFIER_CODE_TEMPLATE = """import typing

from river import base


#  Example INCREMENTAL classifier, returns last seen class
class Classifier{0}(base.Classifier):  # do not change class declaration

    def __init__(self):
        self.last_class = None
        self.classes = set()

    def learn_one(self, x: typing.Dict, y: base.typing.ClfTarget, **kwargs) -> "Classifier{0}":
        self.last_class = y
        self.classes.add(y)
        return self

    def predict_one(self, x: typing.Dict) -> base.typing.ClfTarget:
        return self.last_class

    def predict_proba_one(self, x: typing.Dict) -> typing.Dict[base.typing.ClfTarget, float]:
        probabilities = dict()
        for c in self.classes:
            probabilities[c] = 0
        probabilities[self.last_class] = 1
        return probabilities
"""


def _convert_from_document_to_custom_classifier(custom_classifier: Document) -> CustomClassifier:
    if custom_classifier:
        custom_classifier["id"] = custom_classifier.doc_id
        custom_classifier["created at"] = datetime.fromtimestamp(custom_classifier["created_at"]).strftime(
            "%Y-%m-%d %H:%M:%S")
        custom_classifier["json_schema"] = {
            "title": custom_classifier["name"],
            "type": "object",
            "properties": {
            }
        }
    return custom_classifier


def _locate_id(custom_classifier_id: int, original_custom_classifier_id: typing.Optional[int] = None):
    if original_custom_classifier_id is None:
        original_custom_classifier_id = custom_classifier_id
    return f"cacp.gui.custom.classifiers.classifier{custom_classifier_id}.Classifier{original_custom_classifier_id}"


def _code_path(custom_classifier_id: int) -> Path:
    return CUSTOM_CLASSIFIERS_CODE_DIR.joinpath(f"classifier{custom_classifier_id}.py")


def _save_code(custom_classifier_id: int, code: str):
    with _code_path(custom_classifier_id).open("w") as f:
        f.write(code)


def _remove_code(custom_classifier_id: int):
    _code_path(custom_classifier_id).unlink(missing_ok=True)


def get_all_custom_classifiers() -> List[CustomClassifier]:
    return [_convert_from_document_to_custom_classifier(e) for e in CUSTOM_CLASSIFIERS_DB.all() if e is not None]


def get_custom_classifier(custom_classifier_id: int) -> CustomClassifier:
    return _convert_from_document_to_custom_classifier(CUSTOM_CLASSIFIERS_DB.get(doc_id=custom_classifier_id))


def add_custom_classifier() -> int:
    preview_prevent_modifications()
    new_custom_classifier: CustomClassifier = dict()
    all_classifiers = CUSTOM_CLASSIFIERS_DB.all()
    new_custom_classifier_id = 1 if len(all_classifiers) == 0 else all_classifiers[-1].doc_id + 1
    new_custom_classifier["name"] = f"Custom Classifier {new_custom_classifier_id}"
    new_custom_classifier["type"] = CustomClassifierType.BATCH
    new_custom_classifier["code"] = CUSTOM_CLASSIFIER_BATCH_CODE_TEMPLATE.format(new_custom_classifier_id)
    new_custom_classifier["locate_id"] = _locate_id(new_custom_classifier_id)
    new_custom_classifier["created_at"] = datetime.now().timestamp()
    _save_code(new_custom_classifier_id, new_custom_classifier["code"])
    return CUSTOM_CLASSIFIERS_DB.insert(new_custom_classifier)


def update_custom_classifier(
    custom_classifier_id: int,
    name_value: str,
    type_value: CustomClassifierType,
    code_value: str
):
    preview_prevent_modifications()
    CUSTOM_CLASSIFIERS_DB.update({"name": name_value, "type": type_value, "code": code_value},
                                 doc_ids=[custom_classifier_id])
    _save_code(custom_classifier_id, code_value)


def test_custom_classifier_code(custom_classifier_id: int, code_value: str, type_value: CustomClassifierType):
    preview_prevent_modifications()
    error = None
    _save_code(0, code_value)
    classifier_factory = parse_classifier({"locate_id": _locate_id(0, custom_classifier_id), "code": code_value})

    try:
        ds = ClassificationDataset("iris")
        ds_fold = next(ds.folds())
        if type_value == CustomClassifierType.BATCH:
            process_comparison_single(classifier_factory, "test", ds, ds_fold, DEFAULT_METRICS)
        elif type_value == CustomClassifierType.INCREMENTAL:
            with tempfile.TemporaryDirectory() as tmpdirname:
                process_incremental_comparison_single(
                    classifier_factory, "test",
                    ds, 3, Path(tmpdirname),
                    DEFAULT_INCREMENTAL_METRICS
                )
    except:
        error = traceback.format_exc()

    _remove_code(0)
    return error


def delete_custom_classifier(custom_classifier_id: int):
    preview_prevent_modifications()
    CUSTOM_CLASSIFIERS_DB.remove(doc_ids=[custom_classifier_id])
    _remove_code(custom_classifier_id)
