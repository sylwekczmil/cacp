import contextlib
from functools import lru_cache
from typing import Type, Dict

import sklearn
from sklearn.base import ClassifierMixin
from sklearn.utils import all_estimators

from cacp.gui.external.shared.model import ClassModel, T
from cacp.gui.external.shared.type import to_id


class SklearnClassifierModel(ClassModel):
    name: str
    docs_url: str

    @classmethod
    def base_class(cls):
        return ClassifierMixin

    @classmethod
    def from_class(cls, source_class: Type) -> "SklearnClassifierModel":
        _id = to_id(source_class)
        docs_version_split = str(sklearn.__version__).split(".")
        docs_version = f"{docs_version_split[0]}.{docs_version_split[1]}"
        docs_split = _id.split(".")
        docs_name = ".".join(s for s in docs_split if not s.startswith("_"))
        model = cls(
            id=_id,
            name=source_class.__name__,
            docs_url=f"https://scikit-learn.org/{docs_version}/modules/generated/{docs_name}.html"
        )
        with contextlib.suppress(Exception):
            model.test()
            return model

    @classmethod
    @lru_cache
    def all_dict(cls) -> Dict[str, T]:
        result = {}
        for name, c in all_estimators(type_filter="classifier"):
            if model := cls.from_class(c):
                result[name] = model
        return result
