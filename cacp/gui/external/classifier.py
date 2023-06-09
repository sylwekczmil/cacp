from cacp.gui.external.river_library.classifier import RiverClassifierModel
from cacp.gui.external.sklearn_library.classifier import SklearnClassifierModel


def map_classifiers(classifiers: list):
    return [
        {"#": i + 1, "docs_url": f"[{c.docs_url}]({c.docs_url})", **c.dict()} for
        i, c in
        enumerate(sorted(classifiers, key=lambda c: c.name))
    ]


SKLEARN_CLASSIFIERS = map_classifiers(SklearnClassifierModel.all())
RIVER_CLASSIFIERS = map_classifiers(RiverClassifierModel.all())
