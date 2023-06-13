import dash
from dash import html

from cacp.gui.components.new_experiment.form import NewExperimentForm

dash.register_page(__name__)

layout = html.Div([
    NewExperimentForm()
])
