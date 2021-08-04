from typing import List, Tuple

import dash_table

from spectrominer.corrections.experimental import apply_experimental_corrections
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis


class Table:

    def __init__(self, parser: Parser):
        self.parser = parser

        self.html = dash_table.DataTable(
            id='table',
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            style_header={'text-align': 'center'},
            style_data={'text-align': 'center'},
        )

    def calculate_results(self, metabolite_name: str, selected_rows: List, all_data: bool = False) -> Tuple[List, List]:
        if self.parser.df.empty:
            return [], []

        if all_data:
            analyzes = self.parser.get_analyzes()
        else:
            analyzes = self.parser.get_analyzes_of_given_molecule(metabolite_name)

        if selected_rows:
            control_analyzes = self._find_control_analyzes(analyzes, [])
            with_relative_results = bool(False)  # TODO

            analyzes = apply_experimental_corrections(analyzes, control_analyzes, with_relative_results)

        nbr_of_M = len(analyzes[0].results[0].m_results)

        columns = [{'name': 'Analysis', 'id': 'analysis'}] + [
            {'name': f'M+{i}', 'id': str(i)} for i in range(nbr_of_M)
        ]

        data = []
        for analysis in analyzes:
            values = {'analysis': analysis.name}
            for i, result in enumerate(analysis.results[0].m_results):
                values[str(i)] = f'{result.istd_resp_ratio:.10f}'

            data.append(values)

        return columns, data

    def _find_control_analyzes(self, analyzes: List[Analysis], control_analyzes_indexes: List[int]) -> List[Analysis]:
        control_analyzes = []

        for analysis_index in control_analyzes_indexes:
            for analysis in analyzes:
                if analysis.index == analysis_index:
                    control_analyzes.append(analysis)
                    break

        return control_analyzes
