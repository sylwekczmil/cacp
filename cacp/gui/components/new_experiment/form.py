import uuid
from enum import Enum

import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, State, ctx

from cacp.gui.components.classifiers.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.classifiers.sklearn_classifiers_table import SklearnClassifiersTable
from cacp.gui.components.datasets.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.datasets.river_datasets_table import RiverDatasetsTable
from cacp.gui.components.new_experiment.selected_classifiers_table import SelectedClassifiersTable
from cacp.gui.components.new_experiment.selected_datasets_table import SelectedDatasetsTable
from cacp.gui.components.new_experiment.selection_modal import SelectionModal


class ExperimentType(str, Enum):
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"


class NewExperimentForm(html.Div):
    class ids:
        name_input = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "name-input",
            "aio_id": aio_id
        }
        type_input = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "type-input",
            "aio_id": aio_id
        }
        selected_keel_dataset_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-keel-dataset-store",
            "aio_id": aio_id
        }
        selected_river_dataset_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-river-dataset-store",
            "aio_id": aio_id
        }
        selected_river_classifier_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-river-classifier-store",
            "aio_id": aio_id
        }
        selected_sklearn_classifier_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-sklearn-classifier-store",
            "aio_id": aio_id
        }
        selected_datasets_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-datasets",
            "aio_id": aio_id
        }
        selected_classifiers_store = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "selected-classifiers",
            "aio_id": aio_id
        }
        run_experiment_button = lambda aio_id: {
            "component": "NewExperimentForm",
            "subcomponent": "run-experiment-button",
            "aio_id": aio_id
        }

    ids = ids

    def __init__(
        self,
        aio_id=None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        name_input = html.Div(
            [
                dbc.Label("Name", html_for=self.ids.name_input(aio_id)),
                dbc.Input(id=self.ids.name_input(aio_id), placeholder="Enter name", value=""),
                dbc.FormText(
                    "Provide name for your experiment, it should be unique.",
                    color="secondary",
                ),
            ],
            className="mb-3",
        )

        type_input = html.Div(
            [
                dbc.Label("Type", html_for=self.ids.type_input(aio_id)),
                dbc.RadioItems(
                    {
                        ExperimentType.BATCH: "Batch learning (k-fold Cross-Validation)",
                        ExperimentType.INCREMENTAL: "Incremental learning (Prequential evaluation)"
                    },
                    value=ExperimentType.BATCH,
                    id=self.ids.type_input(aio_id)
                ),
                dbc.FormText(
                    "The choice of the type of experiment determines which classifiers and datasets can be used later.",
                    color="secondary",
                ),
            ],
            className="py-2",
        )

        keel_datasets_button = SelectionModal("Add Keel dataset", KeelDatasetsTable,
                                              self.ids.selected_keel_dataset_store(aio_id))
        river_datasets_button = SelectionModal("Add River dataset", RiverDatasetsTable,
                                               self.ids.selected_river_dataset_store(aio_id),
                                               button_kwargs=dict(className="d-none"))
        river_classifiers_button = SelectionModal("Add River classifiers", RiverClassifiersTable,
                                                  self.ids.selected_river_classifier_store(aio_id),
                                                  button_kwargs=dict(className="d-none"))
        sklearn_classifiers_button = SelectionModal("Add Sklearn classifier", SklearnClassifiersTable,
                                                    self.ids.selected_sklearn_classifier_store(aio_id),
                                                    button_kwargs=dict(className="d-none"))

        selected_datasets_table = SelectedDatasetsTable(store_id=self.ids.selected_datasets_store(aio_id))
        selected_classifiers_table = SelectedClassifiersTable(store_id=self.ids.selected_classifiers_store(aio_id))

        super().__init__([
            html.Div([
                name_input,
                type_input,
                html.Br(),
                html.Div([
                    keel_datasets_button, river_datasets_button,
                ]),
                html.Br(),
                html.H5("Selected datasets"),
                selected_datasets_table,
                html.Br(),
                html.Div([
                    sklearn_classifiers_button, river_classifiers_button,
                ]),
                html.Br(),
                html.H5("Selected classifiers"),
                selected_classifiers_table,
                html.Div([
                    dbc.Button(
                        "Run experiment", id=self.ids.run_experiment_button(aio_id), className="mt-3", n_clicks=0
                    )
                ], className="d-flex justify-content-end align-items-center"),
            ])
        ])

        @callback(
            Output(sklearn_classifiers_button.ids.modal_open_button(sklearn_classifiers_button.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_sklearn_classifiers_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.BATCH else "d-none"

        @callback(
            Output(river_classifiers_button.ids.modal_open_button(river_classifiers_button.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_river_classifiers_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.INCREMENTAL else "d-none"

        @callback(
            Output(river_datasets_button.ids.modal_open_button(river_datasets_button.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_river_datasets_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.INCREMENTAL else "d-none"

        @callback(
            Output(self.ids.selected_classifiers_store(aio_id), "data"),
            Input(self.ids.selected_sklearn_classifier_store(aio_id), "data"),
            Input(self.ids.selected_river_classifier_store(aio_id), "data"),
            Input(selected_classifiers_table.ids.table(selected_classifiers_table.aio_id), "cellRendererData"),
            Input(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_classifiers_store(aio_id), "data")
        )
        def selected_classifier(
            selected_sklearn_classifier_data: list,
            selected_river_classifier_data: list,
            cell_renderer_data: dict,
            _type_value: ExperimentType,
            prev_data: list
        ):
            if ctx.triggered_id == self.ids.type_input(aio_id):
                return []
            elif ctx.triggered_id == self.ids.selected_sklearn_classifier_store(
                aio_id) and selected_sklearn_classifier_data:
                return prev_data + selected_sklearn_classifier_data
            elif ctx.triggered_id == self.ids.selected_river_classifier_store(
                aio_id) and selected_river_classifier_data:
                return prev_data + selected_river_classifier_data
            elif ctx.triggered_id == selected_classifiers_table.ids.table(selected_classifiers_table.aio_id):
                del prev_data[cell_renderer_data["rowIndex"]]
                return prev_data
            return []

        @callback(
            Output(self.ids.selected_datasets_store(aio_id), "data"),
            Input(self.ids.selected_keel_dataset_store(aio_id), "data"),
            Input(self.ids.selected_river_dataset_store(aio_id), "data"),
            Input(selected_datasets_table.ids.table(selected_datasets_table.aio_id), "cellRendererData"),
            Input(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_datasets_store(aio_id), "data")
        )
        def selected_dataset(
            selected_keel_dataset_data: list,
            selected_river_dataset_data: list,
            cell_renderer_data: dict,
            _type_value: ExperimentType,
            prev_data: list
        ):
            if ctx.triggered_id == self.ids.type_input(aio_id):
                return []
            elif ctx.triggered_id == self.ids.selected_keel_dataset_store(
                aio_id) and selected_keel_dataset_data:
                return prev_data + [{**d, "name": d["Name"]} for d in selected_keel_dataset_data]
            elif ctx.triggered_id == self.ids.selected_river_dataset_store(
                aio_id) and selected_river_dataset_data:
                return prev_data + selected_river_dataset_data
            elif ctx.triggered_id == selected_datasets_table.ids.table(selected_datasets_table.aio_id):
                del prev_data[cell_renderer_data["rowIndex"]]
                return prev_data
            return []

        @callback(
            Output(self.ids.run_experiment_button(aio_id), "children"),
            Input(self.ids.run_experiment_button(aio_id), 'n_clicks'),
            State(self.ids.selected_datasets_store(aio_id), "data"),
            State(self.ids.selected_classifiers_store(aio_id), "data"),
        )
        def run_experiment_button(n_clicks, selected_datasets, selected_classifiers):
            if n_clicks:
                print("n_clicks", n_clicks, selected_datasets, selected_classifiers)
            return "Run experiment"
