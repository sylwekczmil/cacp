import dash

from cacp.gui.components.experiments.details.view import ExperimentDetails

dash.register_page(__name__, path_template="/experiment/<experiment_id>")

layout = ExperimentDetails("ed")
