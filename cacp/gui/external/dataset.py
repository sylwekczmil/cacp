from pydoc import locate
from typing import Dict, Callable, cast

from cacp import ClassificationDataset


def parse_dataset(dataset_dict: Dict):
    ds = None
    if "code" in dataset_dict:  # custom dataset
        dataset_type = cast(Callable, locate(dataset_dict["locate_id"], True))
        ds = dataset_type()
    elif dataset_dict["id"] == "cacp.dataset.ClassificationDataset":
        ds = ClassificationDataset(dataset_dict["Name"])
    else:
        dataset_type = cast(Callable, locate(dataset_dict["id"]))
        ds = dataset_type(**dataset_dict["init_values"])

    if not hasattr(ds, "name"):
        ds.name = dataset_dict.get("name", type(ds))
    return ds
