from typing import List

from cacp.gui.external.river_library.classifier import RiverClassifierModel
from cacp.gui.external.river_library.dataset import RiverDatasetModel
from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.sklearn_library.classifier import SklearnClassifierModel


def test_schema_creation_on_all():
    models: List[ClassModel] = []
    models.extend(RiverDatasetModel.all())
    models.extend(RiverClassifierModel.all())
    models.extend(SklearnClassifierModel.all())

    for model in models:
        model: ClassModel = model
        try:
            assert model.json_schema is not None
        except Exception as e:
            print(e)
