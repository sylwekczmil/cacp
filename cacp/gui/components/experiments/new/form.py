from typing import List, Dict

import dash_bootstrap_components as dbc
from dash import html, Output, callback, Input, State, ctx, no_update

from cacp.gui.components.classifiers.custom_classifiers_table import CustomClassifiersTable
from cacp.gui.components.classifiers.river_classifiers_table import RiverClassifiersTable
from cacp.gui.components.classifiers.sklearn_classifiers_table import SklearnClassifiersTable
from cacp.gui.components.datasets.custom_datasets_table import CustomDatasetsTable
from cacp.gui.components.datasets.keel_datasets_table import KeelDatasetsTable
from cacp.gui.components.datasets.river_datasets_table import RiverDatasetsTable
from cacp.gui.components.experiments.new.selected_classifiers_table import SelectedClassifiersTable
from cacp.gui.components.experiments.new.selected_datasets_table import SelectedDatasetsTable
from cacp.gui.components.experiments.new.selected_metrics_table import SelectedMetricsTable
from cacp.gui.components.experiments.new.selection_modal import SelectionModal
from cacp.gui.components.metrics.custom_metrics_table import CustomMetricsTable
from cacp.gui.components.metrics.river_metrics_table import RiverMetricsTable
from cacp.gui.components.metrics.sklearn_metrics_table import SklearnMetricsTable
from cacp.gui.components.shared.utils import global_location_href_output
from cacp.gui.db.experiments import ExperimentType, add_experiment
from cacp.gui.preview import preview_button_kwargs


class NewExperimentForm(html.Div):
    class ids:
        table = lambda aio_id: f"NewExperimentForm-table-{aio_id}"
        name_input = lambda aio_id: f"NewExperimentForm-name_input-{aio_id}"
        type_input = lambda aio_id: f"NewExperimentForm-type_input-{aio_id}"
        selected_datasets_store = lambda aio_id: f"NewExperimentForm-selected_datasets_store-{aio_id}"
        selected_classifiers_store = lambda aio_id: f"NewExperimentForm-selected_classifiers_store-{aio_id}"
        selected_metrics_store = lambda aio_id: f"NewExperimentForm-selected_metrics_store-{aio_id}"
        toast = lambda aio_id: f"NewExperimentForm-toast-{aio_id}"
        create_button = lambda aio_id: f"NewExperimentForm-create_button-{aio_id}"

    ids = ids

    def __init__(
        self,
        aio_id
    ):

        name_input = html.Div(
            [
                dbc.Label("Name", html_for=self.ids.name_input(aio_id)),
                dbc.Input(id=self.ids.name_input(aio_id), placeholder="Enter name"),
                dbc.FormText(
                    "Provide a name for your experiment. It should be unique.",
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
                        ExperimentType.BATCH: "Batch learning (k-fold cross-validation)",
                        ExperimentType.INCREMENTAL: "Incremental learning (prequential evaluation)"
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
        custom_datasets_selection = SelectionModal(
            "Add custom dataset", CustomDatasetsTable, aio_id=f"{aio_id}-kd"
        )
        keel_datasets_selection = SelectionModal(
            "Add KEEL dataset", KeelDatasetsTable, aio_id=f"{aio_id}-cd", button_kwargs=dict(className="mx-2"),
        )
        river_datasets_selection = SelectionModal(
            "Add River dataset", RiverDatasetsTable,
            button_kwargs=dict(className="d-none"), aio_id=f"{aio_id}-rd"
        )
        custom_classifiers_selection = SelectionModal(
            "Add custom classifiers", CustomClassifiersTable, aio_id=f"{aio_id}-cc"
        )
        river_classifiers_selection = SelectionModal(
            "Add River classifiers", RiverClassifiersTable,
            button_kwargs=dict(className="d-none"), aio_id=f"{aio_id}-rc"
        )
        sklearn_classifiers_selection = SelectionModal(
            "Add Sklearn classifier", SklearnClassifiersTable,
            button_kwargs=dict(className="d-none"), aio_id=f"{aio_id}-sc"
        )
        custom_metrics_selection = SelectionModal(
            "Add custom metric", CustomMetricsTable, aio_id=f"{aio_id}-cm"
        )
        river_metrics_selection = SelectionModal(
            "Add River metric", RiverMetricsTable,
            button_kwargs=dict(className="d-none"), aio_id=f"{aio_id}-rm"
        )
        sklearn_metrics_selection = SelectionModal(
            "Add Sklearn metric", SklearnMetricsTable,
            button_kwargs=dict(className="d-none"), aio_id=f"{aio_id}-sm"
        )

        selected_datasets_table = SelectedDatasetsTable(
            store_id=self.ids.selected_datasets_store(aio_id),
            aio_id=aio_id
        )
        selected_classifiers_table = SelectedClassifiersTable(
            store_id=self.ids.selected_classifiers_store(aio_id),
            aio_id=aio_id
        )
        selected_metrics_table = SelectedMetricsTable(
            store_id=self.ids.selected_metrics_store(aio_id),
            aio_id=aio_id
        )

        super().__init__([
            html.Div([
                name_input,
                type_input,
                html.Br(),
                html.Div([
                    custom_datasets_selection, keel_datasets_selection, river_datasets_selection,
                ]),
                html.Br(),
                html.H5("Selected datasets"),
                selected_datasets_table,
                html.Br(),
                html.Div([
                    custom_classifiers_selection, sklearn_classifiers_selection, river_classifiers_selection,
                ]),
                html.Br(),
                html.H5("Selected classifiers"),
                selected_classifiers_table,
                html.Br(),
                html.Div([
                    custom_metrics_selection, sklearn_metrics_selection, river_metrics_selection,
                ]),
                html.Br(),
                html.H5("Selected metrics"),
                selected_metrics_table,
                html.Div([
                    dbc.Button(
                        "Create", id=self.ids.create_button(aio_id), className="mt-3", n_clicks=0,
                        **preview_button_kwargs()
                    )
                ], className="d-flex justify-content-end align-items-center"),
                dbc.Toast(
                    "",
                    id=self.ids.toast(aio_id),
                    header="Validation failed",
                    is_open=False,
                    dismissable=True,
                    duration=5000,
                    icon="danger",
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350, "z-index": "2000"},
                ),
            ])
        ])

        @callback(
            Output(sklearn_classifiers_selection.ids.modal_open_button(sklearn_classifiers_selection.aio_id),
                   "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_sklearn_classifiers_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.BATCH else "d-none"

        @callback(
            Output(sklearn_metrics_selection.ids.modal_open_button(sklearn_metrics_selection.aio_id),
                   "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_sklearn_metricss_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.BATCH else "d-none"

        @callback(
            Output(river_classifiers_selection.ids.modal_open_button(river_classifiers_selection.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_river_classifiers_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.INCREMENTAL else "d-none"

        @callback(
            Output(river_datasets_selection.ids.modal_open_button(river_datasets_selection.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_river_datasets_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.INCREMENTAL else "d-none"

        @callback(
            Output(river_metrics_selection.ids.modal_open_button(river_metrics_selection.aio_id), "className"),
            Input(self.ids.type_input(aio_id), "value"),
        )
        def update_river_metrics_button_class(type_value):
            return "mx-2" if type_value == ExperimentType.INCREMENTAL else "d-none"

        @callback(
            Output(self.ids.selected_classifiers_store(aio_id), "data"),
            Input(custom_classifiers_selection.store_id, "data"),
            Input(sklearn_classifiers_selection.store_id, "data"),
            Input(river_classifiers_selection.store_id, "data"),
            Input(selected_classifiers_table.ids.table(selected_classifiers_table.aio_id), "cellRendererData"),
            Input(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_classifiers_store(aio_id), "data")
        )
        def selected_classifier(
            selected_custom_classifier_data: list,
            selected_sklearn_classifier_data: list,
            selected_river_classifier_data: list,
            cell_renderer_data: dict,
            _type_value: ExperimentType,
            prev_data: list
        ):
            if ctx.triggered_id == self.ids.type_input(aio_id):
                return []
            elif ctx.triggered_id == custom_classifiers_selection.store_id and selected_custom_classifier_data:
                return prev_data + [cc for cc in selected_custom_classifier_data if cc["type"] == _type_value]
            elif ctx.triggered_id == sklearn_classifiers_selection.store_id and selected_sklearn_classifier_data:
                return prev_data + selected_sklearn_classifier_data
            elif ctx.triggered_id == river_classifiers_selection.store_id and selected_river_classifier_data:
                return prev_data + selected_river_classifier_data
            elif ctx.triggered_id == selected_classifiers_table.ids.table(selected_classifiers_table.aio_id):
                del prev_data[cell_renderer_data["rowIndex"]]
                return prev_data
            return no_update

        @callback(
            Output(self.ids.selected_datasets_store(aio_id), "data"),
            Input(custom_datasets_selection.store_id, "data"),
            Input(keel_datasets_selection.store_id, "data"),
            Input(river_datasets_selection.store_id, "data"),
            Input(selected_datasets_table.ids.table(selected_datasets_table.aio_id), "cellRendererData"),
            Input(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_datasets_store(aio_id), "data")
        )
        def selected_dataset(
            selected_custom_dataset_data: list,
            selected_keel_dataset_data: list,
            selected_river_dataset_data: list,
            cell_renderer_data: dict,
            _type_value: ExperimentType,
            prev_data: list
        ):

            if ctx.triggered_id == self.ids.type_input(aio_id):
                return []
            elif ctx.triggered_id == custom_datasets_selection.store_id and selected_custom_dataset_data:
                return prev_data + selected_custom_dataset_data
            elif ctx.triggered_id == keel_datasets_selection.store_id and selected_keel_dataset_data:
                return prev_data + [{**d, "name": d["Name"]} for d in selected_keel_dataset_data]
            elif ctx.triggered_id == river_datasets_selection.store_id and selected_river_dataset_data:
                return prev_data + selected_river_dataset_data
            elif ctx.triggered_id == selected_datasets_table.ids.table(selected_datasets_table.aio_id):
                del prev_data[cell_renderer_data["rowIndex"]]
                return prev_data
            return no_update

        @callback(
            Output(self.ids.selected_metrics_store(aio_id), "data"),
            Input(custom_metrics_selection.store_id, "data"),
            Input(sklearn_metrics_selection.store_id, "data"),
            Input(river_metrics_selection.store_id, "data"),
            Input(selected_metrics_table.ids.table(selected_metrics_table.aio_id), "cellRendererData"),
            Input(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_metrics_store(aio_id), "data")
        )
        def selected_metric(
            selected_custom_metric_data: list,
            selected_sklearn_metric_data: list,
            selected_river_metric_data: list,
            cell_renderer_data: dict,
            _type_value: ExperimentType,
            prev_data: list
        ):

            if ctx.triggered_id == self.ids.type_input(aio_id):
                return []
            elif ctx.triggered_id == custom_metrics_selection.store_id and selected_custom_metric_data:
                return prev_data + selected_custom_metric_data
            elif ctx.triggered_id == sklearn_metrics_selection.store_id and selected_sklearn_metric_data:
                return prev_data + selected_sklearn_metric_data
            elif ctx.triggered_id == river_metrics_selection.store_id and selected_river_metric_data:
                return prev_data + selected_river_metric_data
            elif ctx.triggered_id == selected_metrics_table.ids.table(selected_metrics_table.aio_id):
                del prev_data[cell_renderer_data["rowIndex"]]
                return prev_data
            return no_update

        @callback(
            global_location_href_output(),
            Output(self.ids.toast(aio_id), "children"),
            Output(self.ids.toast(aio_id), "is_open"),
            Input(self.ids.create_button(aio_id), "n_clicks"),
            State(self.ids.name_input(aio_id), "value"),
            State(self.ids.type_input(aio_id), "value"),
            State(self.ids.selected_datasets_store(aio_id), "data"),
            State(self.ids.selected_classifiers_store(aio_id), "data"),
            State(self.ids.selected_metrics_store(aio_id), "data"),
            prevent_initial_call=True,
        )
        def run_experiment_button(
            n_clicks, name_value: str, type_value: ExperimentType, selected_datasets: List[Dict],
            selected_classifiers: List[Dict], selected_metrics: List[Dict]
        ):
            href, toast_message, toast_is_open, = no_update, "", False
            if n_clicks:
                errors = []
                if not name_value:
                    errors.append("Name cannot be empty.")
                if len(selected_datasets) == 0:
                    errors.append("Selecting at least one dataset is required.")
                if len(selected_classifiers) < 2:
                    errors.append("Selecting at least two classifiers is required.")
                if len(selected_metrics) == 0:
                    errors.append("Selecting at least one metric is required.")
                if errors:
                    toast_message = dbc.Alert([html.Div(e) for e in errors], color="danger")
                    toast_is_open = True
                else:
                    experiment_id = add_experiment(name_value, type_value, selected_datasets, selected_classifiers,
                                                   selected_metrics)
                    href = f"/experiment/{experiment_id}"
            return href, toast_message, toast_is_open
