from datetime import datetime

import pandas
import pytest

from spectrominer.analysis import Analysis
from spectrominer.molecule_results import MResult, MoleculeResults
from spectrominer.parser import Parser

RAW_DATA_FILEPATH = './tests/data/raw.csv'


@pytest.fixture
def parser():
    return Parser(RAW_DATA_FILEPATH, delimiter=';')


def test_parser():
    result = Parser(RAW_DATA_FILEPATH, delimiter=';')

    assert type(result.df) == pandas.DataFrame
    assert not result.df.empty
    # Asserting the column format
    assert len(result.df.columns) == 248
    assert len(result.df.columns[0]) == 2
    # Asserting that two-index column selection works
    assert type(result.df[('Lactic acid M+0 Results', 'RT')]) == pandas.Series


def test_get_analysis(parser: Parser):
    result = parser.get_analysis_list()
    print()
    print(result[0].results[0].m_results[0])
    print(result[0].results[0])
    print(result[0])

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert type(result[0].date) == datetime
    assert type(result[0].results[0]) == MoleculeResults
    assert type(result[0].results[0].m_results[0]) == MResult
