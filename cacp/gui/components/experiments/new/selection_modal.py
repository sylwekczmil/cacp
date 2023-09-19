import dash_bootstrap_components as dbc
import dash_rjsf
from dash import html, Output, Input, callback, State, ctx, no_update
from dash.dcc import Store

SUBMIT_BUTTON_OPTIONS_NAME = "ui:submitButtonOptions"


class SelectionModal(html.Span):
    class ids:
        modal_open_button = lambda aio_id: f"SelectionModal-modal_open_button-{aio_id}"
        modal_close_button = lambda aio_id: f"SelectionModal-modal_close_button-{aio_id}"
        modal_add_all_button = lambda aio_id: f"SelectionModal-modal_add_all_button-{aio_id}"
        modal = lambda aio_id: f"SelectionModal-modal-{aio_id}"
        selection_store = lambda aio_id: f"SelectionModal-selection_store-{aio_id}"
        rjsf = lambda aio_id: f"SelectionModal-rjsf-{aio_id}"

    ids = ids

    def __init__(
        self,
        name,
        source_table,
        aio_id,
        button_kwargs=None,
    ):

        if button_kwargs is None:
            button_kwargs = {}

        self.aio_id = aio_id
        self.store_id = f"{aio_id}-store"

        table = source_table(store_id=self.ids.selection_store(aio_id), aio_id=aio_id)

        super().__init__([
            dbc.Button(name, id=self.ids.modal_open_button(aio_id), n_clicks=0, outline=True, color="primary",
                       **button_kwargs),

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(name)),
                    dbc.ModalBody([
                        dbc.Button("Submit all using default properties", id=self.ids.modal_add_all_button(aio_id),
                                   outline=True,
                                   color="primary"),
                        html.Br(),
                        html.Br(),
                        table,
                        html.Br(),
                        dash_rjsf.DashRjsf(
                            id=self.ids.rjsf(aio_id),
                            schema={
                            },
                            uiSchema={SUBMIT_BUTTON_OPTIONS_NAME: {
                                "submitText": "Add",
                                "norender": False,
                                "props": {
                                    "disabled": False,
                                    "className": "rxjs-submit"
                                }
                            }}
                        )
                    ], className="selection-modal-body"),
                    Store(id=self.store_id)
                ],
                id=self.ids.modal(aio_id),
                size="xl",
                is_open=False,
            ),

        ], )

        @callback(
            Output(self.ids.rjsf(aio_id), "value"),
            Output(self.ids.rjsf(aio_id), "schema"),
            Output(self.ids.rjsf(aio_id), "uiSchema"),
            Input(self.ids.selection_store(aio_id), "data")
        )
        def on_table_selection(data):
            if data:
                schema = data[0]["json_schema"]
                if schema["properties"]:
                    schema["title"] = "Provide parameters for " + schema["title"]
                else:
                    schema["title"] = ""
                return None, schema, {SUBMIT_BUTTON_OPTIONS_NAME: {
                    "submitText": "Submit",
                    "norender": False,
                    "props": {
                        "disabled": False,
                        "className": "rxjs-submit"
                    }
                }}
            return None, {}, {SUBMIT_BUTTON_OPTIONS_NAME: {
                "submitText": "Submit",
                "norender": False,
                "props": {
                    "disabled": True,
                    "className": "rxjs-submit"
                }
            }}

        @callback(
            Output(self.store_id, "data"),
            Output(self.ids.modal(aio_id), "is_open"),
            Input(self.ids.rjsf(aio_id), "value"),
            State(self.ids.selection_store(aio_id), "data"),
            Input(self.ids.modal_open_button(aio_id), "n_clicks"),
            Input(self.ids.modal_add_all_button(aio_id), "n_clicks"),
            Input(self.ids.rjsf(aio_id), "n_clicks"),

        )
        def on_open_click_or_selection(values, selected, open_button_n_clicks, _add_all_button_n_clicks,
                                       _values_submit_n_clicks):
            new_data = no_update
            new_modal_is_open = no_update

            if ctx.triggered_id == self.ids.modal_open_button(aio_id) and open_button_n_clicks:
                new_modal_is_open = True

            # add single
            if selected and ctx.triggered_id == self.ids.rjsf(aio_id) and values is not None:
                new_data = [dict(init_values=values, **s) for s in selected]
                # TODO: validate if can be initialized with user params
                new_modal_is_open = False

            # submit all
            if ctx.triggered_id == self.ids.modal_add_all_button(aio_id):
                new_data = [dict(init_values={}, **d) for d in table.data]
                new_modal_is_open = False

            return new_data, new_modal_is_open
