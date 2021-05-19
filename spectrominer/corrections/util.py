import copy
from typing import List

import pandas

from spectrominer.parser.analysis import Analysis
from spectrominer.parser.molecule_results import MoleculeResults


def normalize_analyzes(analyzes: List[Analysis]) -> List[Analysis]:
    analyzes = copy.deepcopy(analyzes)

    for analysis in analyzes:
        for molecule_results in analysis.results:
            sum_of_results = sum_m_results(molecule_results)

            if sum_of_results == 0:
                continue

            for m_result in molecule_results.m_results:
                m_result.istd_resp_ratio /= sum_of_results

    return analyzes


def sum_m_results(molecule_results: MoleculeResults) -> float:
    sum_of_results = 0

    for m_result in molecule_results.m_results:
        if not pandas.isna(m_result.istd_resp_ratio):
            sum_of_results += m_result.istd_resp_ratio

    return sum_of_results
