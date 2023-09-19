from pydoc import locate
from typing import Dict, Callable, cast

from cacp.gui.external.river_library.metric import RiverMetricModel
from cacp.gui.external.sklearn_library.metric import SklearnMetricModel


def map_metric(metrics: list):
    return [
        {"#": i + 1, "docs_url": f"[{c.docs_url}]({c.docs_url})", "json_schema": c.json_schema, **c.dict()} for
        i, c in
        enumerate(sorted(metrics, key=lambda c: c.name))
    ]


def parse_metric(metric_dict: Dict):
    if "code" in metric_dict:  # custom metric
        return cast(Callable, locate(metric_dict["locate_id"], True))
    else:
        return cast(Callable, locate(metric_dict["id"]))


SKLEARN_METRICS = map_metric(SklearnMetricModel.all())
RIVER_METRICS = map_metric(RiverMetricModel.all())
