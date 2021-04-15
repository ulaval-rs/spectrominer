from datetime import datetime

import pandas
import pytest

from spectrominer.parser.analysis import Analysis
from spectrominer.parser.molecule_results import MResult, MoleculeResults
from spectrominer.parser.parser import Parser

RAW_DATA_FILEPATH = './tests/data/raw.csv'
MOLECULE_NAME = 'Lactic acid'


@pytest.fixture
def parser():
    return Parser(RAW_DATA_FILEPATH, delimiter=',')


def test_parser():
    result = Parser(RAW_DATA_FILEPATH, delimiter=',')

    assert type(result.df) == pandas.DataFrame
    assert not result.df.empty
    # Asserting the column format
    assert len(result.df.columns) == 248
    assert len(result.df.columns[0]) == 2
    # Asserting that two-index column selection works
    assert type(result.df[('Lactic acid M+0 Results', 'RT')]) == pandas.Series


def test_get_analysis(parser: Parser):
    result = parser.get_analyzes()

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert type(result[0].date) == datetime
    assert type(result[0].results[0]) == MoleculeResults
    assert type(result[0].results[0].m_results[0]) == MResult
    assert result[0].results[0].m_results[0].istd_resp_ratio == .0001900789525851


def test_get_molecule_names(parser: Parser):
    result = parser.get_molecule_names()

    assert result.sort() == [
        'Fumaric acid', 'cis-Aconitic acid', 'Succinic acid', 'Glutamine', 'Citric acid', 'L-Aspartic acid',
        'L-Glutamic', 'L-Alanine', 'Malic acid', 'L-Pyroglutamic', 'Lactic acid'
    ].sort()


def test_get_analyzes_of_given_molecule(parser: Parser):
    result = parser.get_analyzes_of_given_molecule(MOLECULE_NAME)

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert type(result[0].date) == datetime
    assert type(result[0].results[0]) == MoleculeResults
    assert type(result[0].results[0].m_results[0]) == MResult
    assert result[0].results[0].m_results[0].istd_resp_ratio == 7.70882239116875
    for analysis in result:
        for molecule_result in analysis.results:
            assert molecule_result.name == MOLECULE_NAME
