import contextlib
from functools import lru_cache
from typing import Type, List

import river
from river.metrics.base import ClassificationMetric

from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.shared.type import to_id


class RiverMetricModel(ClassModel):
    name: str
    docs_url: str

    @classmethod
    def base_class(cls):
        return ClassificationMetric

    @classmethod
    @lru_cache
    def all(cls) -> List["RiverMetricModel"]:
        result = []
        for k, v in cls.all_dict().items():
            with contextlib.suppress(NotImplementedError):
                m = v.class_type()
                if hasattr(m, "get") and isinstance(m.get(), float):
                    result.append(v)

        return result

    @classmethod
    def from_class(cls, source_class: Type) -> "RiverMetricModel":
        _id = to_id(source_class)
        docs_split = _id.split(".")
        docs_version = river.__version__
        docs_name = docs_split[3] if len(docs_split) > 3 else docs_split[2]
        return cls(
            id=_id,
            name=source_class.__name__,
            docs_url=f"https://riverml.xyz/{docs_version}/api/{docs_split[1].replace('_', '-')}/{docs_name}/"
        )
