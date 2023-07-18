import dash
import dash_ace
import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, State, no_update
from dash.dcc import Store

from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_classifiers import get_custom_classifier, CustomClassifierType, CustomClassifier, \
    update_custom_classifier, CUSTOM_BATCH_CODE_TEMPLATE, CUSTOM_INCREMENTAL_CODE_TEMPLATE, test_custom_classifier_code

dash.register_page(__name__, path_template="/custom_classifier/<custom_classifier_id>")

CUSTOM_CLASSIFIER_NAME_ID = "custom_classifier_name_id"
CUSTOM_CLASSIFIER_TYPE_ID = "custom_classifier_type_id"
CUSTOM_CLASSIFIER_CODE_ID = "custom_classifier_code_id"
CUSTOM_CLASSIFIER_SAVE_BUTTON_ID = "custom_classifier_save_button_id"
CUSTOM_CLASSIFIER_TOAST_ID = "custom_classifier_toast_id"
CUSTOM_CLASSIFIER_STORE_ID = "custom_classifier_store_id"


def layout(custom_classifier_id=None):
    custom_classifier = get_custom_classifier(custom_classifier_id) if custom_classifier_id else {}

    name_input = html.Div(
        [
            dbc.Label("Name", html_for=CUSTOM_CLASSIFIER_NAME_ID),
            dbc.Input(id=CUSTOM_CLASSIFIER_NAME_ID, placeholder="Enter name", value=custom_classifier.get("name")),
            dbc.FormText(
                "Provide name for your experiment, it should be unique.",
                color="secondary",
            ),
        ],
        className="mb-3",
    )

    type_input = html.Div(
        [
            dbc.Label("Type", html_for=CUSTOM_CLASSIFIER_TYPE_ID),
            dbc.RadioItems(
                {
                    CustomClassifierType.BATCH: "Batch learning",
                    CustomClassifierType.INCREMENTAL: "Incremental learning"
                },
                value=custom_classifier.get("type"),
                id=CUSTOM_CLASSIFIER_TYPE_ID
            )
        ],
        className="py-2",
    )

    code = html.Div(
        [
            dbc.Label("Code", html_for=CUSTOM_CLASSIFIER_NAME_ID), dash_ace.DashAceEditor(
            id=CUSTOM_CLASSIFIER_CODE_ID,
            value=custom_classifier.get("code"),
            theme='github',
            mode='python',
            tabSize=2,
            enableBasicAutocompletion=True,
            placeholder='Python code ...',
            style={"height": "calc(100vh - 400px)", "width": "100%"}
        )])

    save_button = html.Div([
        dbc.Button(
            "Save", id=CUSTOM_CLASSIFIER_SAVE_BUTTON_ID, className="mt-3", n_clicks=0
        )
    ], className="d-flex justify-content-end align-items-center")

    toast = dbc.Toast(
        "",
        id=CUSTOM_CLASSIFIER_TOAST_ID,
        header="Validation failed",
        is_open=False,
        dismissable=True,
        duration=5000,
        icon="danger",
        style={"position": "fixed", "top": 66, "right": 10, "width": 350, "z-index": "2000"},
    )

    store = Store(id=CUSTOM_CLASSIFIER_STORE_ID, data=custom_classifier)

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
    Output(CUSTOM_CLASSIFIER_CODE_ID, "value"),
    Input(CUSTOM_CLASSIFIER_TYPE_ID, "value"),
    State(CUSTOM_CLASSIFIER_STORE_ID, "data"),
    prevent_initial_call=True,
)
def update_river_classifiers_button_class(type_value: CustomClassifierType, classifier: CustomClassifier):
    if type_value == CustomClassifierType.BATCH:
        return CUSTOM_BATCH_CODE_TEMPLATE.format(classifier.get("id"))
    if type_value == CustomClassifierType.INCREMENTAL:
        return CUSTOM_INCREMENTAL_CODE_TEMPLATE.format(classifier.get("id"))
    return no_update


@callback(
    global_location_href_output(),
    Output(CUSTOM_CLASSIFIER_TOAST_ID, "children"),
    Output(CUSTOM_CLASSIFIER_TOAST_ID, "is_open"),
    Input(CUSTOM_CLASSIFIER_SAVE_BUTTON_ID, "n_clicks"),
    State(CUSTOM_CLASSIFIER_NAME_ID, "value"),
    State(CUSTOM_CLASSIFIER_TYPE_ID, "value"),
    State(CUSTOM_CLASSIFIER_CODE_ID, "value"),
    State(CUSTOM_CLASSIFIER_STORE_ID, "data"),
    prevent_initial_call=True,
)
def save_button_click(
    n_clicks, name_value: str, type_value: CustomClassifierType, code_value: str, custom_classifier: CustomClassifier
):
    href, toast_message, toast_is_open, = no_update, "", False
    if n_clicks:
        custom_classifier_id = int(custom_classifier["id"])
        errors = []
        if not name_value:
            errors.append("Name can not be empty.")

        test_error = test_custom_classifier_code(custom_classifier_id, code_value, type_value)
        if test_error:
            errors.append(test_error)

        if errors:
            toast_message = dbc.Alert([html.Div(e) for e in errors], color="danger")
            toast_is_open = True
        else:
            update_custom_classifier(custom_classifier_id, name_value, type_value, code_value)
    return href, toast_message, toast_is_open
