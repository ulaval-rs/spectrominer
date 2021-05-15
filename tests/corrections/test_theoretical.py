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
    with pytest.raises(NotImplementedError):
        apply_theoretical_corrections(analyzes)
