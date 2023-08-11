import dash
from dash import html

from cacp.gui.components.metrics.river_metrics_table import RiverMetricsTable
from cacp.gui.components.metrics.sklearn_metrics_table import SklearnMetricsTable

dash.register_page(__name__)

layout = html.Div([
    html.H5("Custom metrics"),
    html.H5("Wrapped Sklearn metrics (BATCH)", className="mt-4"),
    html.P(
        "To ensure operation on as many data sets as possible the metrics have been wrapped. "
        "Default parameters if occurred were set to average='weighted' and zero_division=0."),
    SklearnMetricsTable("smt"),
    html.H5("River metrics (INCREMENTAL)", className="mt-4"),
    RiverMetricsTable("rmt"),
])
