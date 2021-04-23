import copy
from typing import List

import pandas

from spectrominer.parser.molecule_results import MoleculeResults

CORRECTION_MATRICES = {
    'lactic acid': [
        [1.1714235469, 0, 0, 0],
        [-0.143275149, 1.1714235469, 0, 0],
        [-0.0357412341, -0.143275149, 1.1714235469, 0],
        [0.0070255799, -0.0357412341, -0.143275149, 1.1714235469]
    ]
}


def apply_corrections(molecule_results: MoleculeResults) -> MoleculeResults:
    # TODO: remove background noise

    # Normalization
    sum_of_m_results = _sum_of_m_results(molecule_results)
    for m_result in molecule_results.m_results:
        # To get relative proportion
        m_result.istd_resp_ratio = m_result.istd_resp_ratio / sum_of_m_results

    # Applying correction matrix (gives proportional distribution)
    correction_matrix = _find_correction_matrix(molecule_results.name)
    molecule_results = _apply_correction_matrix(correction_matrix, molecule_results)

    # TODO
    # Going back to absolute
    for m_result in molecule_results.m_results:
        # To get relative ion amounts
        m_result.istd_resp_ratio = m_result.istd_resp_ratio * sum_of_m_results

        # To get absolute proportion bg140

    return molecule_results


def _sum_of_m_results(molecule_results: MoleculeResults) -> float:
    sum_of_m_results = 0

    for m_result in molecule_results.m_results:
        if not pandas.isna(m_result.istd_resp_ratio):
            sum_of_m_results += m_result.istd_resp_ratio

    return sum_of_m_results


def _find_correction_matrix(molecule_name: str) -> List[List[float]]:
    return CORRECTION_MATRICES[molecule_name.lower()]


def _apply_correction_matrix(
        correction_matrix: List[List[float]],
        molecule_results: MoleculeResults) -> MoleculeResults:
    molecule_results_tmp = copy.deepcopy(molecule_results)
    nbr_of_M = len(molecule_results.m_results)

    for m_result in molecule_results.m_results:
        m_result.istd_resp_ratio = 0

        for i in range(nbr_of_M):
            m_result.istd_resp_ratio += molecule_results_tmp.m_results[i].istd_resp_ratio * \
                                        correction_matrix[i][m_result.m_number]

    return molecule_results
