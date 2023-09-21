from pathlib import Path

import dash
import dash_ace
import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, State, no_update
from dash.dcc import Store

from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_datasets import get_custom_dataset, CustomDatasetType, CustomDataset, \
    update_custom_dataset, CUSTOM_DATASET_CODE_TEMPLATE, \
    test_custom_dataset_code, KEEL_DATASET_CODE_TEMPLATE, CSV_DATASET_CODE_TEMPLATE
from cacp.gui.preview import preview_button_kwargs

dash.register_page(__name__, path_template="/custom_dataset/<custom_dataset_id>")

CUSTOM_DATASET_NAME_ID = "custom_dataset_name_id"
CUSTOM_DATASET_TYPE_ID = "custom_dataset_type_id"
CUSTOM_DATASET_PATH_ID = "custom_dataset_path_id"
CUSTOM_DATASET_PATH_DIV_ID = "custom_dataset_path_div_id"
CUSTOM_DATASET_CODE_ID = "custom_dataset_code_id"
CUSTOM_DATASET_CODE_DIV_ID = "custom_dataset_code_div_id"
CUSTOM_DATASET_SAVE_BUTTON_ID = "custom_dataset_save_button_id"
CUSTOM_DATASET_TOAST_ID = "custom_dataset_toast_id"
CUSTOM_DATASET_STORE_ID = "custom_dataset_store_id"
CODE_HEIGHT = {"height": "calc(100vh - 450px)", "width": "100%"}
CODE_HEIGHT_INVISIBLE = {"height": "0", "width": "100%", "visibility": "hidden"}


def layout(custom_dataset_id=None):
    custom_dataset = get_custom_dataset(custom_dataset_id) if custom_dataset_id else {}

    name_input = html.Div(
        [
            dbc.Label("Name", html_for=CUSTOM_DATASET_NAME_ID),
            dbc.Input(id=CUSTOM_DATASET_NAME_ID, placeholder="Enter name", value=custom_dataset.get("name")),
            dbc.FormText(
                "Provide name for your dataset, it should be unique.",
                color="secondary",
            ),
        ],
        className="mb-3",
    )

    type_input = html.Div(
        [
            dbc.Label("Type", html_for=CUSTOM_DATASET_TYPE_ID),
            dbc.RadioItems(
                {
                    CustomDatasetType.CUSTOM_CODE: "Custom code",
                    CustomDatasetType.CSV_FILE: "CSV file (last column will be treated as class column)",
                    CustomDatasetType.KEEL_FILES: "KEEL files (should have KEEL datasets structure)"
                },
                value=custom_dataset.get("type"),
                id=CUSTOM_DATASET_TYPE_ID
            )
        ],
        className="py-2",
    )

    path_input = html.Div(
        [
            dbc.Label("Path", html_for=CUSTOM_DATASET_PATH_ID),
            dbc.Input(id=CUSTOM_DATASET_PATH_ID, placeholder="Enter path", value=custom_dataset.get("path")),
        ],
        id=CUSTOM_DATASET_PATH_DIV_ID,
        className="d-none",
    )

    code = html.Div(
        [
            dbc.Label("Code", html_for=CUSTOM_DATASET_NAME_ID), dash_ace.DashAceEditor(
            id=CUSTOM_DATASET_CODE_ID,
            value=custom_dataset.get("code"),
            theme='github',
            mode='python',
            tabSize=2,
            enableBasicAutocompletion=True,
            placeholder='Python code ...',
            style={"height": "calc(100% - 30px)", "width": "100%"}
        )],
        id=CUSTOM_DATASET_CODE_DIV_ID,
        style=CODE_HEIGHT
    )

    save_button = html.Div([
        dbc.Button(
            "Save", id=CUSTOM_DATASET_SAVE_BUTTON_ID, className="mt-3", n_clicks=0, **preview_button_kwargs()
        )
    ], className="d-flex justify-content-end align-items-center")

    toast = dbc.Toast(
        "",
        id=CUSTOM_DATASET_TOAST_ID,
        header="Validation failed",
        is_open=False,
        dismissable=True,
        duration=5000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350, "z-index": "2000"},
    )

    store = Store(id=CUSTOM_DATASET_STORE_ID, data=custom_dataset)

    view = html.Div([
        name_input,
        type_input,
        path_input,
        code,
        save_button,
        toast,
        store
    ])

    return view


@callback(
    Output(CUSTOM_DATASET_PATH_DIV_ID, "className"),
    Input(CUSTOM_DATASET_TYPE_ID, "value"),
)
def update_path_display(type_value: CustomDatasetType):
    return "d-none" if type_value == CustomDatasetType.CUSTOM_CODE else "py-4"


@callback(
    Output(CUSTOM_DATASET_CODE_ID, "value"),
    Output(CUSTOM_DATASET_CODE_DIV_ID, "style"),
    Input(CUSTOM_DATASET_TYPE_ID, "value"),
    Input(CUSTOM_DATASET_NAME_ID, "value"),
    Input(CUSTOM_DATASET_PATH_ID, "value"),
    State(CUSTOM_DATASET_STORE_ID, "data")
)
def update_river_datasets_button_class(type_value: CustomDatasetType, name: str, path: str, dataset: CustomDataset):
    if dash.ctx.triggered_id == CUSTOM_DATASET_TYPE_ID:
        if type_value == CustomDatasetType.CUSTOM_CODE:
            return CUSTOM_DATASET_CODE_TEMPLATE.format(dataset.get("id")), CODE_HEIGHT
        if type_value == CustomDatasetType.CSV_FILE:
            return CSV_DATASET_CODE_TEMPLATE.format(dataset.get("id"), name, path), CODE_HEIGHT_INVISIBLE
        if type_value == CustomDatasetType.KEEL_FILES:
            return KEEL_DATASET_CODE_TEMPLATE.format(dataset.get("id"), name, path), CODE_HEIGHT_INVISIBLE

    if type_value == CustomDatasetType.CSV_FILE:
        return CSV_DATASET_CODE_TEMPLATE.format(dataset.get("id"), name, path), CODE_HEIGHT_INVISIBLE
    if type_value == CustomDatasetType.KEEL_FILES:
        return KEEL_DATASET_CODE_TEMPLATE.format(dataset.get("id"), name, path), CODE_HEIGHT_INVISIBLE
    return no_update, no_update


@callback(
    global_location_href_output(),
    Output(CUSTOM_DATASET_TOAST_ID, "children"),
    Output(CUSTOM_DATASET_TOAST_ID, "header"),
    Output(CUSTOM_DATASET_TOAST_ID, "is_open"),
    Input(CUSTOM_DATASET_SAVE_BUTTON_ID, "n_clicks"),
    State(CUSTOM_DATASET_NAME_ID, "value"),
    State(CUSTOM_DATASET_TYPE_ID, "value"),
    State(CUSTOM_DATASET_CODE_ID, "value"),
    State(CUSTOM_DATASET_PATH_ID, "value"),
    State(CUSTOM_DATASET_STORE_ID, "data"),
    prevent_initial_call=True,
)
def save_button_click(
    n_clicks, name_value: str, type_value: CustomDatasetType, code_value: str, path_value: str,
    custom_dataset: CustomDataset
):
    href, toast_message, toast_header, toast_is_open, = no_update, "", no_update, False
    if n_clicks:
        custom_dataset_id = int(custom_dataset["id"])
        errors = []
        if not name_value:
            errors.append("Name can not be empty.")

        if type_value != CustomDatasetType.CUSTOM_CODE:
            path = Path(path_value)
            if type_value == CustomDatasetType.CSV_FILE and not path.exists():
                errors.append("Path is invalid, should be existing file.")
            if type_value == CustomDatasetType.KEEL_FILES and (not path.exists() or not path.is_dir()):
                errors.append("Path is invalid for KEEL dataset, should be existing directory.")

        if not errors:
            test_error = test_custom_dataset_code(custom_dataset_id, name_value, code_value)
            if test_error:
                errors.append(test_error)

        if errors:
            toast_message = dbc.Alert([html.Div(e) for e in errors], color="danger")
            toast_header = "Validation error"
        else:
            update_custom_dataset(custom_dataset_id, name_value, type_value, code_value, path_value)
            toast_message = dbc.Alert(html.Div("Saved"))
            toast_header = "Success"
        toast_is_open = True
    return href, toast_message, toast_header, toast_is_open
