import uuid

import dash_bootstrap_components as dbc
import dash_rjsf
from dash import html, Output, Input, callback, State, ctx, no_update
from dash.dcc import Store


class SelectionModal(html.Span):
    class ids:
        modal_open_button = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'dataset-modal-open-button',
            'aio_id': aio_id
        }
        modal_close_button = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'dataset-modal-close-button',
            'aio_id': aio_id
        }
        modal_add_all_button = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'dataset-modal-add-all-button',
            'aio_id': aio_id
        }
        modal = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'dataset-modal',
            'aio_id': aio_id
        }
        selection_store = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'selection-store',
            'aio_id': aio_id
        }
        rjsf = lambda aio_id: {
            'component': 'AddSelectionModal',
            'subcomponent': 'rjsf',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        name,
        source_table,
        store_id,
        aio_id=None,
        button_kwargs=None,
    ):

        if aio_id is None:
            self.aio_id = str(uuid.uuid4())
        if button_kwargs is None:
            button_kwargs = {}

        self.store_id = store_id

        table = source_table(store_id=self.ids.selection_store(self.aio_id))

        super().__init__([
            dbc.Button(name, id=self.ids.modal_open_button(self.aio_id), n_clicks=0, outline=True, color="primary",
                       **button_kwargs),

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(name)),
                    dbc.ModalBody([
                        dbc.Button("Submit all using default properties", id=self.ids.modal_add_all_button(self.aio_id),
                                   outline=True,
                                   color="primary"),
                        html.Br(),
                        html.Br(),
                        table,
                        html.Br(),
                        dash_rjsf.DashRjsf(
                            id=self.ids.rjsf(self.aio_id),
                            schema={
                            },
                            uiSchema={"ui:submitButtonOptions": {
                                "submitText": "Submit",
                                "norender": False,
                                "props": {
                                    "disabled": False,
                                    "className": "rxjs-submit"
                                }
                            }}
                        )
                    ]),
                    Store(id=self.store_id)
                ],
                id=self.ids.modal(self.aio_id),
                size="xl",
                is_open=False,
            ),

        ], )

        @callback(
            Output(self.ids.rjsf(self.aio_id), 'schema'),
            Output(self.ids.rjsf(self.aio_id), 'uiSchema'),
            Input(self.ids.selection_store(self.aio_id), 'data')
        )
        def on_table_selection(data):
            if data:
                schema = data[0]["json_schema"]
                if schema['properties']:
                    schema['title'] = "Provide parameters for " + schema['title']
                else:
                    schema['title'] = ""
                return schema, {"ui:submitButtonOptions": {
                    "submitText": "Submit",
                    "norender": False,
                    "props": {
                        "disabled": False,
                        "className": "rxjs-submit"
                    }
                }}
            return {}, {"ui:submitButtonOptions": {
                "submitText": "Submit",
                "norender": False,
                "props": {
                    "disabled": True,
                    "className": "rxjs-submit"
                }
            }}

        @callback(
            Output(self.store_id, 'data'),
            Output(self.ids.modal(self.aio_id), "is_open"),
            Input(self.ids.rjsf(self.aio_id), 'value'),
            State(self.ids.selection_store(self.aio_id), 'data'),
            Input(self.ids.modal_open_button(self.aio_id), "n_clicks"),
            Input(self.ids.modal_add_all_button(self.aio_id), "n_clicks"),
            Input(self.ids.rjsf(self.aio_id), 'n_clicks'),

        )
        def on_open_click_or_selection(values, selected, open_button_n_clicks, _add_all_button_n_clicks,
                                       _values_submit_n_clicks):
            new_data = no_update
            new_modal_is_open = no_update

            if ctx.triggered_id == self.ids.modal_open_button(self.aio_id) and open_button_n_clicks:
                new_modal_is_open = True

            if ctx.triggered_id == self.ids.rjsf(self.aio_id):
                new_data = [dict(init_values=values, **s) for s in selected]
                new_modal_is_open = False

            if ctx.triggered_id == self.ids.modal_add_all_button(self.aio_id):
                new_data = [dict(init_values={}, **d) for d in table.data]
                new_modal_is_open = False

            return new_data, new_modal_is_open
