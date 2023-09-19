from cacp.gui.external.river_library.metric import RiverMetricModel
from cacp.gui.external.sklearn_library.metric import SklearnMetricModel


def test_list_keel_metrics():
    assert len(RiverMetricModel.all()) == 34


def test_list_sklearn_classifiers():
    assert len(SklearnMetricModel.all()) == 6
