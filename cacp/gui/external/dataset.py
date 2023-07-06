from pydoc import locate
from typing import Dict, Callable, cast

from cacp import ClassificationDataset


def parse_dataset(dataset_dict: Dict):
    if dataset_dict["id"] == "cacp.dataset.ClassificationDataset":
        return ClassificationDataset(dataset_dict["Name"])
    else:
        dataset_type = cast(Callable, locate(dataset_dict["id"]))
        return dataset_type(**dataset_dict["init_values"])
