from typing import List

import pytest

from spectrominer.corrections.util import normalize_analyzes, sum_m_results
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis
from spectrominer.parser.molecule_results import MoleculeResults

RAW_DATA_FILEPATH = './tests/data/raw-data-example-1.csv'


@pytest.fixture
def analyzes():
    parser = Parser(RAW_DATA_FILEPATH, delimiter=',')
    analyzes = parser.get_analyzes_of_given_molecule('Lactic acid')

    return analyzes


@pytest.fixture
def molecule_results(analyzes: List[Analysis]):
    for analysis in analyzes:
        for molecule_result in analysis.results:
            return molecule_result


def test_normalize_analyzes(analyzes: List[Analysis]):
    result = normalize_analyzes(analyzes)

    assert sum(m.istd_resp_ratio for m in result[0].results[0].m_results) == 1.0


@pytest.mark.parametrize('expected', [11.355803329660874])
def test_sum_m_results(molecule_results: MoleculeResults, expected):
    result = sum_m_results(molecule_results)

    assert result == expected
