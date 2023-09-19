from functools import lru_cache
from typing import Type, List

import river
from river.base import Classifier

from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.shared.type import to_id


class RiverClassifierModel(ClassModel):
    name: str
    docs_url: str

    @classmethod
    def base_class(cls):
        return Classifier

    @classmethod
    @lru_cache
    def all(cls) -> List["RiverClassifierModel"]:
        return [c for c in cls.all_dict().values() if "Base" not in c.name]

    @classmethod
    def from_class(cls, source_class: Type) -> "RiverClassifierModel":
        _id = to_id(source_class)
        docs_split = _id.split(".")
        docs_version = river.__version__
        docs_name = docs_split[3] if len(docs_split) > 3 else docs_split[2]
        return cls(
            id=_id,
            name=source_class.__name__,
            docs_url=f"https://riverml.xyz/{docs_version}/api/{docs_split[1].replace('_', '-')}/{docs_name}/"
        )
