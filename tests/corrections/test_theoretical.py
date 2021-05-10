import copy
from typing import List

import pytest

from spectrominer.corrections.theoretical import apply_theoretical_corrections
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis

RAW_DATA_FILEPATH = './tests/data/raw-data-example-1.csv'


@pytest.fixture
def analyzes():
    parser = Parser(RAW_DATA_FILEPATH, delimiter=',')
    analyzes = parser.get_analyzes_of_given_molecule('Lactic acid')

    return analyzes


def test_theoretical_corrections(analyzes: List[Analysis]):
    result = apply_theoretical_corrections(copy.deepcopy(analyzes))

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert result[0].name == 'CW-387 milieu #1 Gluc C13'
    assert result[0].results[0].name == 'Lactic acid'
    assert result[0].results[0].m_results[0].m_number == 0
    assert result[0].results[0].m_results[0].istd_resp_ratio == 7.867682981815292
    assert analyzes[0].results[0].m_results[0].istd_resp_ratio != \
           result[0].results[0].m_results[0].istd_resp_ratio
