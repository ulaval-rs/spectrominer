from typing import List

import pandas

from spectrominer.parser.analysis import Analysis
from spectrominer.parser.molecule_results import MResult, MoleculeResults
from spectrominer.parser.util import decode_date


class Parser:

    def __init__(self, filepath: str, delimiter: str = ',', quotechar: str = '"') -> None:
        self.df = pandas.read_csv(
            filepath,
            delimiter=delimiter,
            quotechar=quotechar,
            header=[0, 1]
        )

    def get_analyzes(self) -> List[Analysis]:
        self._remove_empty_columns()
        self._fill_column_names()

        analysis_list = []

        for index, row in self.df.iterrows():
            molecules_results = self._get_molecules_results(index)

            analysis_list.append(
                Analysis(
                    index=index,
                    name=row[('Sample', 'Name')],
                    date=decode_date(row[('Sample', 'Acq. Date-Time')]),
                    results=molecules_results
                )
            )

        analysis_list.sort()

        return analysis_list

    def get_molecule_names(self) -> List[str]:
        # Multiple label and multiple molecules: set('Lactic acid M+1, Lactic acid M+2, ..., Malic acid M+0, ...)
        molecules_labels = set(column[0] for column in self.df.columns if 'Results' in column[0])
        # Multiple label per molecule set('Lactic acid M+1, Lactic acid M+2, ..., Malic acid M+0, ...)
        molecule_names = set(label.split('M+')[0].strip() for label in molecules_labels if 'M+' in label)

        return list(molecule_names)

    def get_analyzes_of_given_molecule(self, molecule_name: str) -> List[Analysis]:
        analyzes_of_given_molecules = self.get_analyzes()

        for analysis in analyzes_of_given_molecules:
            analysis.results = [r for r in analysis.results if r.name == molecule_name]

        return analyzes_of_given_molecules

    def _get_molecules_results(self, row_index: int) -> List[MoleculeResults]:
        molecules_results = []

        molecule_names = self.get_molecule_names()

        # Multiple label and multiple molecules: set('Lactic acid M+1, Lactic acid M+2, ..., Malic acid M+0, ...)
        molecules_labels = set(column[0] for column in self.df.columns if 'Results' in column[0])

        for name in molecule_names:
            # Getting all labels with the molecule name
            molecule_labels = [label for label in molecules_labels if name in label]
            # Removing results label without the "M+"
            molecule_labels = [label for label in molecule_labels if 'M+' in label]

            if not molecule_labels:
                continue

            m_results = []

            for label in molecule_labels:
                m_number = int(label.split('M+')[1].split(' ')[0])  # Example of label: "L-Pyroglutamic M+2 Results"

                m_results.append(
                    MResult(
                        m_number=m_number,
                        retention_time=float(self.df[(label, 'RT')].iloc[[row_index]]),
                        area=float(self.df[(label, 'Area')].iloc[[row_index]]),
                        istd_resp_ratio=float(self.df[(label, 'ISTD Resp. Ratio')].iloc[[row_index]]),
                    )
                )

            m_results.sort()
            molecules_results.append(MoleculeResults(name=name, m_results=m_results))

        molecules_results.sort()

        return molecules_results

    def _fill_column_names(self) -> None:
        """
        Extend the column name to all following column without name

        --------------       -----------
        name | no_name       name | name
        RT   | Area     -->  RT   | Area
        --------------       -----------
        """
        new_columns = []
        last_column_name = self.df.columns[0][0]

        for column in self.df.columns:
            if 'Unnamed:' in column[0]:
                column = (last_column_name, column[1])
            else:
                last_column_name = column[0]

            new_columns.append(column)

        self.df.columns = new_columns

    def _remove_empty_columns(self) -> None:
        columns_to_remove = []

        for column in self.df.columns:
            if 'Unnamed:' in column[0] and 'Unnamed:' in column[1]:
                columns_to_remove.append(column)

        for column in columns_to_remove:
            del self.df[column]
