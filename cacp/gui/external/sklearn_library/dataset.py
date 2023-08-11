from enum import Enum
from typing import Optional, Type

import river
from river.datasets.base import Dataset, SyntheticDataset

from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.shared.type import to_id


class RiverDataSetType(str, Enum):
    SYNTHETIC = "Synthetic"
    REAL = "Real"

    @classmethod
    def from_river_dataset(cls, river_dataset: Dataset):
        if issubclass(river_dataset.__class__, SyntheticDataset):
            return cls.SYNTHETIC
        else:
            return cls.REAL

    def docs_path(self):
        docs_version = river.__version__
        docs_api_sub_path = "synth" if self == RiverDataSetType.SYNTHETIC else "datasets"
        return f"https://riverml.xyz/{docs_version}/api/{docs_api_sub_path}/"


class DatasetModel(ClassModel):
    name: str
    type: RiverDataSetType
    task: str
    samples: int
    features: int
    outputs: Optional[int] = None
    classes: Optional[int] = None
    docs_path: str

    @classmethod
    def base_class(cls):
        return Dataset

    @classmethod
    def from_class(cls, source_class: Type) -> "DatasetModel":
        river_dataset: Dataset = source_class()
        dataset_repr = river_dataset._repr_content

        def parse_int_field(value):
            return int(dataset_repr.get(value, "0").replace("∞", "0").replace(",", ""))

        dataset_name = dataset_repr.get("Name")
        dataset_type = RiverDataSetType.from_river_dataset(river_dataset)

        task = dataset_repr.get("Task")
        classes = parse_int_field("Classes")
        if classes == 0 and task == "Binary classification":
            classes = 2

        return cls(
            id=to_id(source_class),
            name=dataset_name,
            type=dataset_type,
            task=dataset_repr.get("Task"),
            samples=parse_int_field("Samples"),
            features=parse_int_field("Features"),
            outputs=parse_int_field("Outputs"),
            classes=classes,
            docs_path=dataset_type.docs_path() + dataset_name
        )
