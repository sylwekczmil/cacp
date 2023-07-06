import dash

from cacp.gui.components.experiments.new.form import NewExperimentForm

dash.register_page(__name__)

layout = NewExperimentForm("ef")
