import os

import dash
import dash_core_components as core
import dash_html_components as html
from dash.dependencies import Input, Output

from spectrominer.parser import Parser
from spectrominer.web.file_selection import FileSelector
from spectrominer.web.table import Table

STYLESHEET_FILEPATH = os.path.join(
    os.path.dirname(__file__),
    'assets/style.css'
)


def make_web_app() -> dash.Dash:
    # Services
    parser = Parser()

    # UI
    file_selector = FileSelector(parser)
    table = Table(parser)

    # Main app
    app = dash.Dash('Spectrominer')
    app.css.config.serve_locally = False
    app.css.append_css({'external_url': STYLESHEET_FILEPATH})

    app.layout = html.Div(
        children=[
            html.H1('Spectrominer'),
            file_selector.html,
            html.Hr(),
            html.Div([
                core.Dropdown(
                    id='cb-metabolite',
                    placeholder='Select the metabolite...',
                    clearable=False,
                    style={
                        'width': '50%',
                        'margin': 'auto',
                    }
                ),
            ]),
            html.Br(),
            table.html,
        ],
        style={
            'text-align': 'center'
        }
    )

    # Callbacks
    app.callback(
        Output('cb-metabolite', 'options'),
        Input('upload-data', 'contents'),
    )(file_selector.file_has_been_selected)

    app.callback(
        Output('table', 'columns'),
        Output('table', 'data'),
        Input('cb-metabolite', 'value'),
        Input('table', 'selected_rows'),
    )(table.calculate_results)

    return app
