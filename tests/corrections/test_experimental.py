import copy
from typing import List

import pytest

from spectrominer.corrections.experimental import apply_experimental_corrections,\
    _calculate_average_control_analysis,_remove_control_analyzes_from_analyzes
from spectrominer.parser import Parser
from spectrominer.parser.analysis import Analysis

RAW_DATA_FILEPATH = './tests/data/raw-data-example-1.csv'


@pytest.fixture
def analyzes():
    parser = Parser(RAW_DATA_FILEPATH, delimiter=',')
    analyzes = parser.get_analyzes_of_given_molecule('Lactic acid')

    return analyzes


@pytest.fixture
def control_analyzes():
    control_analyzes = []

    parser = Parser(RAW_DATA_FILEPATH, delimiter=',')
    analyzes = parser.get_analyzes_of_given_molecule('Lactic acid')

    for analysis in analyzes:
        if 'milieu' in analysis.name:
            control_analyzes.append(analysis)

    return control_analyzes


def test_experimental_corrections(analyzes: List[Analysis], control_analyzes: List[Analysis]):
    result = apply_experimental_corrections(copy.deepcopy(analyzes), control_analyzes)

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert result[0].name == 'CW-387 organoides tube #10 Gluc C13'
    assert result[0].results[0].name == 'Lactic acid'
    assert result[0].results[0].m_results[0].m_number == 0
    assert result[0].results[0].m_results[0].istd_resp_ratio == -5.458194729447245
    assert analyzes[0].results[0].m_results[0].istd_resp_ratio != \
           result[0].results[0].m_results[0].istd_resp_ratio


def test_remove_control_analyzes_from_analyzes(analyzes: List[Analysis], control_analyzes: List[Analysis]):
    result = _remove_control_analyzes_from_analyzes(analyzes, control_analyzes)

    assert type(result) == list
    analyzes_names = [r.name for r in result]
    for analysis in result:
        assert analysis.name in analyzes_names


def test_calculate_average_control_analysis(control_analyzes: List[Analysis]):
    result = _calculate_average_control_analysis(control_analyzes)

    assert type(result) == Analysis
    assert result.name == 'Average control analysis'
    assert result.results[0].name == 'Lactic acid'
    assert result.results[0].m_results[0].m_number == 0
    assert result.results[0].m_results[0].istd_resp_ratio == 8.673349226255805
    assert result.results[0].m_results[1].m_number == 1
    assert result.results[0].m_results[1].istd_resp_ratio == 1.9557995002186628


