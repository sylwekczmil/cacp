from typing import Type

import river
from river.base import Classifier

from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.shared.type import class_to_id


class RiverClassifierModel(ClassModel):
    name: str
    docs_url: str

    @classmethod
    def base_class(cls):
        return Classifier

    @classmethod
    def from_class(cls, source_class: Type) -> 'RiverClassifierModel':
        _id = class_to_id(source_class)
        docs_split = _id.split('.')
        docs_version = river.__version__
        docs_name = docs_split[3] if len(docs_split) > 3 else docs_split[2]
        return cls(
            id=_id,
            name=source_class.__name__,
            docs_url=f'https://riverml.xyz/{docs_version}/api/{docs_split[1].replace("_", "-")}/{docs_name}/'
        )
