import dash
from dash import html, callback, Input, no_update

from cacp.gui.components.metrics.custom_metrics_table import CustomMetricsTable
from cacp.gui.components.metrics.river_metrics_table import RiverMetricsTable
from cacp.gui.components.metrics.sklearn_metrics_table import SklearnMetricsTable
from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_metrics import add_custom_metric
from cacp.gui.preview import preview_button_kwargs

dash.register_page(__name__)

ADD_CUSTOM_CLASSIFIER_BUTTON_ID = "add_custom_metric_button"

layout = html.Div([
    html.Div(
        html.Button("Add custom metric", className="btn btn-primary", id=ADD_CUSTOM_CLASSIFIER_BUTTON_ID,
                    **preview_button_kwargs()),
        className="d-flex justify-content-end mb-4"),
    html.H5("Custom metrics"),
    CustomMetricsTable("cmt"),
    html.H5("Wrapped Sklearn metrics (BATCH)", className="mt-4"),
    html.P(
        "To ensure operation on as many data sets as possible the metrics have been wrapped. "
        "Default parameters if occurred were set to average='weighted' and zero_division=0."),
    SklearnMetricsTable("smt"),
    html.H5("River metrics (INCREMENTAL)", className="mt-4"),
    RiverMetricsTable("rmt"),
])


@callback(
    global_location_href_output(),
    Input(ADD_CUSTOM_CLASSIFIER_BUTTON_ID, "n_clicks"),
    prevent_initial_call=True,
)
def add_custom_metric_button(n_clicks):
    if n_clicks:
        custom_metric_id = add_custom_metric()
        return f"/custom_metric/{custom_metric_id}"
    return no_update
