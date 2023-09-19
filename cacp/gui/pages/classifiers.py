import dash
from dash import html, callback, Input, no_update

from cacp.gui.components.classifiers.custom_classifiers_table import CustomClassifiersTable
from cacp.gui.components.classifiers.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.classifiers.sklearn_classifiers_table import SklearnClassifiersTable
from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.custom_classifiers import add_custom_classifier
from cacp.gui.preview import preview_button_kwargs

dash.register_page(__name__)

ADD_CUSTOM_CLASSIFIER_BUTTON_ID = "add_custom_classifier_button"

layout = html.Div([
    html.Div(
        html.Button("Add custom classifier", className="btn btn-primary", id=ADD_CUSTOM_CLASSIFIER_BUTTON_ID,
                    **preview_button_kwargs()),
        className="d-flex justify-content-end mb-4"),
    html.H5("Custom classifiers"),
    CustomClassifiersTable("cct"),
    html.H5("Sklearn classifiers (BATCH)", className="mt-4"),
    SklearnClassifiersTable("sct"),
    html.H5("River classifiers (INCREMENTAL)", className="mt-4"),
    RiverClassifiersTable("rct"),
])


@callback(
    global_location_href_output(),
    Input(ADD_CUSTOM_CLASSIFIER_BUTTON_ID, "n_clicks"),
    prevent_initial_call=True,
)
def add_custom_classifier_button(n_clicks):
    if n_clicks:
        custom_classifier_id = add_custom_classifier()
        return f"/custom_classifier/{custom_classifier_id}"
    return no_update
