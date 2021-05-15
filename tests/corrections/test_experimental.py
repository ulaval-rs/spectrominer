import copy
from typing import List

import pytest

from spectrominer.corrections.experimental import _calculate_average_control_analysis, \
    _convert_results_in_absolute, _find_number_of_values_per_m_result_per_molecule, \
    _remove_control_analyzes_from_analyzes, \
    _remove_relative_abundance, apply_experimental_corrections
from spectrominer.corrections.util import normalize_analyzes
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


@pytest.fixture
def normalized_analyzes(analyzes):
    normalized_analyzes = normalize_analyzes(analyzes)

    return normalized_analyzes


@pytest.fixture
def normalized_averaged_control_analysis(control_analyzes):
    normalized_analyzes = normalize_analyzes(control_analyzes)

    return _calculate_average_control_analysis(normalized_analyzes)


@pytest.fixture
def relative_analyzes(normalized_analyzes, normalized_averaged_control_analysis):
    analyzes = _remove_relative_abundance(
        normalized_analyzes,
        normalized_averaged_control_analysis
    )

    return analyzes


def test_experimental_corrections(analyzes: List[Analysis], control_analyzes: List[Analysis]):
    result = apply_experimental_corrections(copy.deepcopy(analyzes), control_analyzes)

    assert type(result) == list
    assert type(result[0]) == Analysis
    assert result[0].name == 'CW-387 organoides tube #10 Gluc C13'
    assert result[0].results[0].name == 'Lactic acid'
    assert result[0].results[0].m_results[0].m_number == 0
    assert result[0].results[0].m_results[0].istd_resp_ratio == 7.70882239116875
    # Assert M+0 has not change
    assert analyzes[0].results[0].m_results[0].istd_resp_ratio == result[0].results[0].m_results[0].istd_resp_ratio
    # Assert M+1 is lesser (because natural abundance has been removed)
    assert analyzes[0].results[0].m_results[1].istd_resp_ratio > result[0].results[0].m_results[1].istd_resp_ratio


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


def test_find_number_of_values_per_m_result_per_molecule(control_analyzes: List[Analysis]):
    result = _find_number_of_values_per_m_result_per_molecule(control_analyzes)

    assert list(result.keys()) == ['Lactic acid']
    assert list(result['Lactic acid'].keys()) == [0, 1, 2, 3]
    # Assert the number of non-NaN for each M+*
    assert result['Lactic acid'][0] == 8
    assert result['Lactic acid'][1] == 8
    assert result['Lactic acid'][2] == 8
    assert result['Lactic acid'][3] == 8


def test_remove_relative_abundance(normalized_analyzes: List[Analysis], normalized_averaged_control_analysis: Analysis):
    result = _remove_relative_abundance(normalized_analyzes, normalized_averaged_control_analysis)

    assert type(result[0]) == Analysis
    assert result[0].results[0].name == 'Lactic acid'
    assert result[0].results[0].m_results[0].m_number == 0
    assert result[0].results[0].m_results[0].istd_resp_ratio == 0.4288443025456099
    assert result[0].results[0].m_results[1].m_number == 1
    assert result[0].results[0].m_results[1].istd_resp_ratio == -0.026574901065229944


def test_convert_results_in_absolute(relative_analyzes: List[Analysis], normalized_analyzes: List[Analysis], analyzes: List[Analysis]):
    result = _convert_results_in_absolute(relative_analyzes, normalized_analyzes, analyzes)

    assert type(result[0]) == Analysis
    assert result[0].results[0].name == 'Lactic acid'
    # Result should not be normalized
    assert sum(m.istd_resp_ratio for m in result[0].results[0].m_results) != 1.0
