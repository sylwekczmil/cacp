from __future__ import annotations

from typing import List

from river.neighbors import KNNClassifier
from sklearn.neighbors import KNeighborsClassifier

from cacp.gui.external.river_library.classifier import RiverClassifierModel
from cacp.gui.external.river_library.dataset import RiverDatasetModel
from cacp.gui.external.shared.model import ClassModel
from cacp.gui.external.shared.schema import parse_model
from cacp.gui.external.sklearn_library.classifier import SklearnClassifierModel


def test_schema_creation_on_all():
    models: List[ClassModel] = []
    models.extend(RiverDatasetModel.all())
    models.extend(RiverClassifierModel.all())
    models.extend(SklearnClassifierModel.all())

    for model in models:
        assert model.json_schema is not None


def test_river_knn_classifier():
    model = parse_model(KNNClassifier)
    schema = model.schema()
    assert schema == {'title': 'KNNClassifier', 'type': 'object',
                      'properties': {'n_neighbors': {'title': 'N Neighbors', 'default': 5, 'type': 'integer'},
                                     'weighted': {'title': 'Weighted', 'default': True, 'type': 'boolean'},
                                     'cleanup_every': {'title': 'Cleanup Every', 'default': 0, 'type': 'integer'},
                                     'softmax': {'title': 'Softmax', 'default': False, 'type': 'boolean'}}}


def test_sklearn_knn_classifier():
    model = parse_model(KNeighborsClassifier)
    schema = model.schema()
    assert schema == {'title': 'KNeighborsClassifier', 'type': 'object',
                      'properties': {'n_neighbors': {'title': 'N Neighbors', 'default': 5, 'type': 'integer'},
                                     'leaf_size': {'title': 'Leaf Size', 'default': 30, 'type': 'integer'},
                                     'p': {'title': 'P', 'default': 2, 'type': 'integer'},
                                     'n_jobs': {'title': 'N Jobs', 'type': 'integer'}}}


def test_simple_schema():
    class Test1:
        def __init__(self, number: int, number_fields: List[float], or_field: int | None, or_field2: int | float = 1):
            self.number = number
            self.number_fields = number_fields
            self.or_field = or_field
            self.or_field2 = or_field2

    model = parse_model(Test1)
    schema = model.schema()
    assert schema == {'title': 'Test1', 'type': 'object',
                      'properties': {'number': {'title': 'Number', 'type': 'integer'},
                                     'number_fields': {'title': 'Number Fields', 'type': 'array',
                                                       'items': {'type': 'number'}},
                                     'or_field': {'title': 'Or Field', 'type': 'integer'},
                                     'or_field2': {'title': 'Or Field2', 'default': 1,
                                                   'anyOf': [{'type': 'integer'}, {'type': 'number'}]}}}
