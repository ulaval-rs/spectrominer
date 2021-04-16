import pandas

from spectrominer.parser.molecule_results import MoleculeResults


def apply_corrections(molecule_results: MoleculeResults) -> MoleculeResults:
    sum_of_m_results = _sum_of_m_results(molecule_results)

    for m_result in molecule_results.m_results:
        # To get relative proportion
        m_result.istd_resp_ratio = m_result.istd_resp_ratio / sum_of_m_results

        # TODO: Removing background noise
        m_result.istd_resp_ratio = m_result.istd_resp_ratio * 1

    return molecule_results


def _sum_of_m_results(molecule_results: MoleculeResults) -> float:
    sum_of_m_results = 0

    for m_result in molecule_results.m_results:
        if not pandas.isna(m_result.istd_resp_ratio):
            sum_of_m_results += m_result.istd_resp_ratio

    return sum_of_m_results
