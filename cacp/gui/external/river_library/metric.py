from typing import Type

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


if __name__ == '__main__':
    me = RiverMetricModel.all()
    print(me)
