import base64
import io
from typing import Dict, List, Optional

import dash_core_components as core
import dash_html_components as html

from spectrominer.parser import Parser


class FileSelector:

    def __init__(self, parser: Parser):
        self.parser = parser

        self.html = core.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '80%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': 'auto'
            },
            multiple=False
        )

    def file_has_been_selected(self, content: str) -> List[Dict]:
        if not content:
            return []

        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        self.parser.parse(io.BytesIO(decoded), content_type=content_type)

        return [{'label': name, 'value': name} for name in self.parser.get_molecule_names()]
