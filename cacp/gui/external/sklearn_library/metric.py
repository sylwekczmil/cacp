from functools import lru_cache
from typing import Dict, List

from cacp.gui.external.shared.model import T, BaseAppModel
from cacp.gui.external.shared.type import to_id
from cacp.util import matthews_corrcoef, auc, accuracy, precision, recall, f1

METRICS = (
    ("AUC", auc, "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html"),
    ("Accuracy", accuracy, "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html"),
    ("Precision", precision, "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html"),
    ("Recall", recall, "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html"),
    ("F1", f1, "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html"),
    ("Matthews correlation coefficient", matthews_corrcoef,
     "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html")
)


class SklearnMetricModel(BaseAppModel):
    id: str
    name: str
    docs_url: str

    @property
    def json_schema(self):
        return {"title": self.name, "type": "object", "properties": {}}

    @classmethod
    @lru_cache
    def all_dict(cls) -> Dict[str, T]:
        result = {}
        for name, function, docs_url in METRICS:
            model_id = to_id(function)
            result[model_id] = cls(
                id=model_id,
                name=name,
                docs_url=docs_url
            )

        return result

    @classmethod
    @lru_cache
    def all(cls) -> List[T]:
        return list(cls.all_dict().values())

    @classmethod
    @lru_cache
    def get_by_id(cls, _id: str) -> T:
        return cls.all_dict().get(_id)
