import dash
import dash_rjsf
from dash import html, Output, Input
from river.tree import ExtremelyFastDecisionTreeClassifier

from cacp.gui.external.river_library.classifier import RiverClassifierModel

dash.register_page(__name__, path="/")

layout = html.Content([
    dash_rjsf.DashRjsf(
        id="input",
        schema=RiverClassifierModel.from_class(ExtremelyFastDecisionTreeClassifier).json_schema,
    ),
    html.Div("", id="output")
])


@dash.callback(Output("output", "children"), [Input("input", "value")])
def display_output(value):
    print("You have entered {}".format(value))
