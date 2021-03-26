from typing import List

import pandas

from spectrominer.analysis import Analysis
from spectrominer.util import decode_date


class Parser:

    def __init__(self, filepath: str, delimiter: str = ',', quotechar: str = '"') -> None:
        self.df = pandas.read_csv(
            filepath,
            delimiter=delimiter,
            quotechar=quotechar,
            header=[0, 1]
        )

    def get_analysis_list(self) -> List[Analysis]:
        analysis_data = self.df[[
            ('Unnamed: 3_level_0', 'Name'),
            ('Unnamed: 7_level_0', 'Acq. Date-Time'),
        ]]

        analysis_list = []

        for i, row in analysis_data.iterrows():
            analysis_list.append(
                Analysis(
                    index=i,
                    name=row[('Unnamed: 3_level_0', 'Name')],
                    date=decode_date(row[('Unnamed: 7_level_0', 'Acq. Date-Time')])
                )
            )

        print(analysis_list[0])

        return analysis_list
