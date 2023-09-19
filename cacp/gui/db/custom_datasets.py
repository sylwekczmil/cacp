import tempfile
import traceback
import typing
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TypedDict, List

from river.dummy import NoChangeClassifier
from sklearn.dummy import DummyClassifier
from tinydb import TinyDB
from tinydb.table import Document

from cacp.comparison import process_comparison_single, DEFAULT_METRICS, process_incremental_comparison_single, \
    DEFAULT_INCREMENTAL_METRICS
from cacp.gui.custom.datasets import CUSTOM_DATASETS_CODE_DIR
from cacp.gui.external.dataset import parse_dataset
from cacp.gui.preview import preview_prevent_modifications


class CustomDatasetType(str, Enum):
    CUSTOM_CODE = "CUSTOM_CODE"
    CSV_FILE = "CSV_FILE"
    KEEL_FILES = "KEEL_FILES"


class CustomDataset(TypedDict):
    id: int
    locate_id: str
    name: str
    type: CustomDatasetType
    code: str
    path: typing.Optional[str]
    created_at: float


CUSTOM_DATASETS_DB = TinyDB(CUSTOM_DATASETS_CODE_DIR / "datasets.json")
CUSTOM_DATASET_CODE_TEMPLATE = """import typing

import numpy as np
from sklearn.model_selection import KFold

from cacp import ClassificationDatasetMinimalBase, ClassificationFoldData
from cacp.dataset import AVAILABLE_N_FOLDS


class Dataset{}(ClassificationDatasetMinimalBase):  # do not change class declaration

    def folds(
        self,
        n_folds: AVAILABLE_N_FOLDS = 10,
        dob_scv: bool = True,
        categorical_to_numerical=True
    ) -> typing.Iterable[ClassificationFoldData]:  # do not change method declaration

        # change code below

        classes = 2
        features = 5
        instances = 100

        labels = np.array([label for label in range(classes)])
        x = np.random.rand(instances, features)
        y = np.random.choice(classes, instances)
        kf = KFold(n_splits=n_folds)

        folds = []

        for i, (train_index, test_index) in enumerate(kf.split(x), start=1):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            folds.append(ClassificationFoldData(
                index=i,
                labels=labels,
                x_test=x_test,
                y_test=y_test,
                x_train=x_train,
                y_train=y_train
            ))

        return iter(folds)
"""

KEEL_DATASET_CODE_TEMPLATE = """from pathlib import Path

from cacp import LocalClassificationDataset


class Dataset{}(LocalClassificationDataset):

    def __init__(self):
        super().__init__("{}", Path(r"{}"))
"""

CSV_DATASET_CODE_TEMPLATE = """from pathlib import Path

from cacp import LocalCsvClassificationDataset


class Dataset{}(LocalCsvClassificationDataset):

    def __init__(self):
        super().__init__("{}", Path(r"{}"))
"""


def _convert_from_document_to_custom_dataset(custom_dataset: Document) -> CustomDataset:
    if custom_dataset:
        custom_dataset["id"] = custom_dataset.doc_id
        custom_dataset["created at"] = datetime.fromtimestamp(custom_dataset["created_at"]).strftime(
            "%Y-%m-%d %H:%M:%S")
        custom_dataset["json_schema"] = {
            "title": custom_dataset["name"],
            "type": "object",
            "properties": {
            }
        }
    return custom_dataset


def _locate_id(custom_dataset_id: int, original_custom_dataset_id: typing.Optional[int] = None):
    if original_custom_dataset_id is None:
        original_custom_dataset_id = custom_dataset_id

    return f"cacp.gui.custom.datasets.dataset{custom_dataset_id}.Dataset{original_custom_dataset_id}"


def _code_path(custom_dataset_id: int) -> Path:
    return CUSTOM_DATASETS_CODE_DIR.joinpath(f"dataset{custom_dataset_id}.py")


def _save_code(custom_dataset_id: int, code: str):
    with _code_path(custom_dataset_id).open("w") as f:
        f.write(code)


def _remove_code(custom_dataset_id: int):
    _code_path(custom_dataset_id).unlink(missing_ok=True)


def get_all_custom_datasets() -> List[CustomDataset]:
    return [_convert_from_document_to_custom_dataset(e) for e in CUSTOM_DATASETS_DB.all() if e is not None]


def get_custom_dataset(custom_dataset_id: int) -> CustomDataset:
    return _convert_from_document_to_custom_dataset(CUSTOM_DATASETS_DB.get(doc_id=custom_dataset_id))


def add_custom_dataset() -> int:
    preview_prevent_modifications()
    new_custom_dataset: CustomDataset = dict()
    all_datasets = CUSTOM_DATASETS_DB.all()
    new_custom_dataset_id = 1 if len(all_datasets) == 0 else all_datasets[-1].doc_id + 1
    new_custom_dataset["name"] = f"Custom Dataset {new_custom_dataset_id}"
    new_custom_dataset["type"] = CustomDatasetType.CUSTOM_CODE
    new_custom_dataset["code"] = CUSTOM_DATASET_CODE_TEMPLATE.format(new_custom_dataset_id)
    new_custom_dataset["locate_id"] = _locate_id(new_custom_dataset_id)
    new_custom_dataset["created_at"] = datetime.now().timestamp()
    _save_code(new_custom_dataset_id, new_custom_dataset["code"])
    return CUSTOM_DATASETS_DB.insert(new_custom_dataset)


def update_custom_dataset(
    custom_dataset_id: int,
    name_value: str,
    type_value: CustomDatasetType,
    code_value: str,
    path_value: typing.Optional[str] = None
):
    preview_prevent_modifications()
    CUSTOM_DATASETS_DB.update({"name": name_value, "type": type_value, "code": code_value,
                               "path": path_value, "locate_id": _locate_id(custom_dataset_id)},
                              doc_ids=[custom_dataset_id])
    _save_code(custom_dataset_id, code_value)


def test_custom_dataset_code(custom_dataset_id: int, name_value: str, code_value: str):
    preview_prevent_modifications()
    error = None
    _save_code(0, code_value)
    try:
        ds = parse_dataset(
            {"name": name_value, "locate_id": _locate_id(0, custom_dataset_id), "code": code_value}
        )
        ds_fold = next(ds.folds())

        #  count classes
        labels = set()
        for _, y in ds:
            labels.add(y)
        number_of_classes = len(labels)

        # test if works for BATCH
        process_comparison_single(lambda n_inputs, n_classes: DummyClassifier(), "test", ds, ds_fold, DEFAULT_METRICS)

        # test if works for INCREMENTAL
        with tempfile.TemporaryDirectory() as tmpdirname:
            process_incremental_comparison_single(
                lambda n_inputs, n_classes: NoChangeClassifier(), "test",
                ds, number_of_classes, Path(tmpdirname), DEFAULT_INCREMENTAL_METRICS
            )
    except:
        error = traceback.format_exc()

    _remove_code(0)
    return error


def delete_custom_dataset(custom_dataset_id: int):
    preview_prevent_modifications()
    CUSTOM_DATASETS_DB.remove(doc_ids=[custom_dataset_id])
    _remove_code(custom_dataset_id)
