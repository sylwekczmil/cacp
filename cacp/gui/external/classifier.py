from pydoc import locate
from typing import Dict, Callable, cast

from cacp.gui.external.river_library.classifier import RiverClassifierModel
from cacp.gui.external.sklearn_library.classifier import SklearnClassifierModel


def map_classifiers(classifiers: list):
    return [
        {"#": i + 1, "docs_url": f"[{c.docs_url}]({c.docs_url})", "json_schema": c.json_schema, **c.dict()} for
        i, c in
        enumerate(sorted(classifiers, key=lambda c: c.name))
    ]


SKLEARN_CLASSIFIERS = map_classifiers(SklearnClassifierModel.all())
RIVER_CLASSIFIERS = map_classifiers(RiverClassifierModel.all())


def parse_classifier(classifier_dict: Dict):
    if "code" in classifier_dict:  # custom classifier
        classifier_type = cast(Callable, locate(classifier_dict["locate_id"], True))
        return lambda n_inputs, n_classes: classifier_type()
    else:
        classifier_type = cast(Callable, locate(classifier_dict["id"]))
        return lambda n_inputs, n_classes: classifier_type(**classifier_dict["init_values"])
