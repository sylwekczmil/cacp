import dash
import dash_ace
import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, State, no_update
from dash.dcc import Store

from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_metrics import get_custom_metric, CustomMetricType, CustomMetric, \
    update_custom_metric, CUSTOM_METRIC_BATCH_CODE_TEMPLATE, CUSTOM_INCREMENTAL_METRIC_CODE_TEMPLATE, \
    test_custom_metric_code
from cacp.gui.preview import preview_button_kwargs

dash.register_page(__name__, path_template="/custom_metric/<custom_metric_id>")

CUSTOM_METRIC_NAME_ID = "custom_metric_name_id"
CUSTOM_METRIC_TYPE_ID = "custom_metric_type_id"
CUSTOM_METRIC_CODE_ID = "custom_metric_code_id"
CUSTOM_METRIC_SAVE_BUTTON_ID = "custom_metric_save_button_id"
CUSTOM_METRIC_TOAST_ID = "custom_metric_toast_id"
CUSTOM_METRIC_STORE_ID = "custom_metric_store_id"


def layout(custom_metric_id=None):
    custom_metric = get_custom_metric(custom_metric_id) if custom_metric_id else {}

    name_input = html.Div(
        [
            dbc.Label("Name", html_for=CUSTOM_METRIC_NAME_ID),
            dbc.Input(id=CUSTOM_METRIC_NAME_ID, placeholder="Enter name", value=custom_metric.get("name")),
            dbc.FormText(
                "Provide name for your metric, it should be unique.",
                color="secondary",
            ),
        ],
        className="mb-3",
    )

    type_input = html.Div(
        [
            dbc.Label("Type", html_for=CUSTOM_METRIC_TYPE_ID),
            dbc.RadioItems(
                {
                    CustomMetricType.BATCH: "Batch learning",
                    CustomMetricType.INCREMENTAL: "Incremental learning"
                },
                value=custom_metric.get("type"),
                id=CUSTOM_METRIC_TYPE_ID
            )
        ],
        className="py-2",
    )

    code = html.Div(
        [
            dbc.Label("Code", html_for=CUSTOM_METRIC_NAME_ID), dash_ace.DashAceEditor(
            id=CUSTOM_METRIC_CODE_ID,
            value=custom_metric.get("code"),
            theme='github',
            mode='python',
            tabSize=2,
            enableBasicAutocompletion=True,
            placeholder='Python code ...',
            style={"height": "calc(100vh - 400px)", "width": "100%"}
        )])

    save_button = html.Div([
        dbc.Button(
            "Save", id=CUSTOM_METRIC_SAVE_BUTTON_ID, className="mt-3", n_clicks=0, **preview_button_kwargs()
        )
    ], className="d-flex justify-content-end align-items-center")

    toast = dbc.Toast(
        "",
        id=CUSTOM_METRIC_TOAST_ID,
        header="Validation failed",
        is_open=False,
        dismissable=True,
        duration=5000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350, "z-index": "2000"},
    )

    store = Store(id=CUSTOM_METRIC_STORE_ID, data=custom_metric)

    view = html.Div([
        name_input,
        type_input,
        code,
        save_button,
        toast,
        store
    ])

    return view


@callback(
    Output(CUSTOM_METRIC_CODE_ID, "value"),
    Input(CUSTOM_METRIC_TYPE_ID, "value"),
    State(CUSTOM_METRIC_STORE_ID, "data"),
    prevent_initial_call=True,
)
def update_river_metrics_button_class(type_value: CustomMetricType, metric: CustomMetric):
    if type_value == CustomMetricType.BATCH:
        return CUSTOM_METRIC_BATCH_CODE_TEMPLATE.format(metric.get("id"))
    if type_value == CustomMetricType.INCREMENTAL:
        return CUSTOM_INCREMENTAL_METRIC_CODE_TEMPLATE.format(metric.get("id"))
    return no_update


@callback(
    global_location_href_output(),
    Output(CUSTOM_METRIC_TOAST_ID, "children"),
    Output(CUSTOM_METRIC_TOAST_ID, "header"),
    Output(CUSTOM_METRIC_TOAST_ID, "is_open"),
    Input(CUSTOM_METRIC_SAVE_BUTTON_ID, "n_clicks"),
    State(CUSTOM_METRIC_NAME_ID, "value"),
    State(CUSTOM_METRIC_TYPE_ID, "value"),
    State(CUSTOM_METRIC_CODE_ID, "value"),
    State(CUSTOM_METRIC_STORE_ID, "data"),
    prevent_initial_call=True,
)
def save_button_click(
    n_clicks, name_value: str, type_value: CustomMetricType, code_value: str, custom_metric: CustomMetric
):
    href, toast_message, toast_header, toast_is_open, = no_update, "", no_update, False
    if n_clicks:
        custom_metric_id = int(custom_metric["id"])
        errors = []
        if not name_value:
            errors.append("Name can not be empty.")

        test_error = test_custom_metric_code(custom_metric_id, code_value, type_value)
        if test_error:
            errors.append(test_error)

        if errors:
            toast_message = dbc.Alert([html.Div(e) for e in errors], color="danger")
            toast_header = "Validation error"
        else:
            update_custom_metric(custom_metric_id, name_value, type_value, code_value)
            toast_message = dbc.Alert(html.Div("Saved"))
            toast_header = "Success"
        toast_is_open = True
    return href, toast_message, toast_header, toast_is_open
