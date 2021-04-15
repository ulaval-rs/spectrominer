import pytest

from spectrominer.corrections import apply_corrections
from spectrominer.parser import Parser
from spectrominer.parser.molecule_results import MoleculeResults

RAW_DATA_FILEPATH = './tests/data/raw.csv'


@pytest.fixture
def molecule_results():
    parser = Parser(RAW_DATA_FILEPATH, delimiter=',')
    analyzes = parser.get_analyzes_of_given_molecule('Lactic acid')

    return analyzes[0].results[0]


def test_corrections(molecule_results: MoleculeResults):
    result = apply_corrections(molecule_results)

    assert type(result) == MoleculeResults
    assert molecule_results.m_results[0].istd_resp_ratio != result.m_results[0].istd_resp_ratio