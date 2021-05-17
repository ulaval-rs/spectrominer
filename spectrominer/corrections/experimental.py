import copy
from typing import Dict, List

import numpy

from spectrominer.corrections.util import normalize_analyzes
from spectrominer.parser.analysis import Analysis


def apply_experimental_corrections(
        analyzes: List[Analysis],
        control_analyzes: List[Analysis],
        with_relative_results: bool) -> List[Analysis]:
    original_analyzes = copy.deepcopy(analyzes)
    analyzes = _remove_control_analyzes_from_analyzes(analyzes, control_analyzes)

    # Normalization
    normalized_analyzes = normalize_analyzes(analyzes)

    normalized_control_analyzes = normalize_analyzes(control_analyzes)
    normalized_averaged_control_analysis = _calculate_average_control_analysis(normalized_control_analyzes)

    # Getting the proportion of M+* values (relative results)
    analyzes = _remove_relative_abundance(normalized_analyzes, normalized_averaged_control_analysis)

    # Getting the absolute values of the presence of M+* results
    if with_relative_results:
        return _remove_negative_values(analyzes)

    return _convert_results_in_absolute(analyzes, normalized_analyzes, original_analyzes)


def _remove_control_analyzes_from_analyzes(
        analyzes: List[Analysis],
        control_analyzes: List[Analysis]) -> List[Analysis]:
    for control_analysis in control_analyzes:
        analyzes.remove(control_analysis)

    return analyzes


def _calculate_average_control_analysis(control_analyzes: List[Analysis]) -> Analysis:
    average_control_analysis = control_analyzes[0]
    average_control_analysis.name = 'Average control analysis'

    number_of_values_per_m_result_per_molecule = _find_number_of_values_per_m_result_per_molecule(control_analyzes)

    # Sum on all the values
    for i, analysis in enumerate(control_analyzes):
        # The first analysis will be the average.
        if i == 0:
            continue

        for molecule_results in analysis.results:
            for m_result in molecule_results.m_results:
                # If value is NaN, no need to add it
                if numpy.isnan(m_result.istd_resp_ratio):
                    continue

                if numpy.isnan(average_control_analysis[molecule_results.name][m_result.m_number].istd_resp_ratio):
                    average_control_analysis[molecule_results.name][
                        m_result.m_number].istd_resp_ratio = m_result.istd_resp_ratio
                else:
                    average_control_analysis[molecule_results.name][
                        m_result.m_number].istd_resp_ratio += m_result.istd_resp_ratio

    # Dividing by the number of analyzes to get the average
    for molecule_results in average_control_analysis.results:
        for m_result in molecule_results.m_results:
            # These values are useless
            m_result.retention_time = numpy.NaN
            m_result.area = numpy.NaN

            if number_of_values_per_m_result_per_molecule[molecule_results.name][m_result.m_number] == 0:
                raise ValueError(f'{molecule_results.name} M+{m_result.m_number} has no control values')

            m_result.istd_resp_ratio /= number_of_values_per_m_result_per_molecule[
                molecule_results.name][m_result.m_number]

    return average_control_analysis


def _find_number_of_values_per_m_result_per_molecule(analyzes: List[Analysis]) -> Dict[str, Dict[int, int]]:
    number_of_values_per_m_result_per_molecule: Dict[str, Dict[int, int]] = {}

    for analysis in analyzes:
        for molecule_results in analysis.results:
            number_of_values_per_m_result_per_molecule[molecule_results.name] = {
                m_result.m_number: 0 for m_result in molecule_results.m_results
            }

    for analysis in analyzes:
        for molecule_results in analysis.results:
            for m_result in molecule_results.m_results:
                if not numpy.isnan(m_result.istd_resp_ratio):
                    number_of_values_per_m_result_per_molecule[molecule_results.name][m_result.m_number] += 1

    return number_of_values_per_m_result_per_molecule


def _remove_relative_abundance(
        normalized_analyzes: List[Analysis],
        normalized_averaged_control_analysis: Analysis) -> List[Analysis]:
    analyzes = copy.deepcopy(normalized_analyzes)

    for analysis in analyzes:
        for molecule_result, control_molecule_results in zip(analysis.results,
                                                             normalized_averaged_control_analysis.results):
            assert molecule_result.name == control_molecule_results.name, 'Molecule should be the same, since molecules are sorted by name'

            for m_result, control_m_result in zip(molecule_result.m_results, control_molecule_results.m_results):
                assert m_result.m_number == control_m_result.m_number, 'M+ number should be the same, since they are sorted'

                # When M+0, remove the natural fraction of C13 (all other M+*)
                if m_result.m_number == 0:
                    m_result.istd_resp_ratio = m_result.istd_resp_ratio - sum(
                        m.istd_resp_ratio for m in control_molecule_results.m_results
                    ) / len(control_molecule_results.m_results)

                else:
                    m_result.istd_resp_ratio -= control_m_result.istd_resp_ratio

    return analyzes


def _convert_results_in_absolute(
        relative_analyzes: List[Analysis],
        normalized_analyzes: List[Analysis],
        original_analyzes: List[Analysis]) -> List[Analysis]:
    analyzes = relative_analyzes

    for analysis, normalized_analysis, original_analysis in zip(analyzes, normalized_analyzes, original_analyzes):
        for molecule_result, normalized_molecule_result, original_molecule_result in zip(analysis.results,
                                                                                         normalized_analysis.results,
                                                                                         original_analysis.results):
            for m_result, normalized_m_result, original_m_result in zip(molecule_result.m_results,
                                                                        normalized_molecule_result.m_results,
                                                                        original_molecule_result.m_results):
                if m_result.m_number == 0:
                    m_result.istd_resp_ratio = original_m_result.istd_resp_ratio

                elif m_result.istd_resp_ratio < 0:
                    m_result.istd_resp_ratio = 0

                else:
                    m_result.istd_resp_ratio = m_result.istd_resp_ratio * original_m_result.istd_resp_ratio / normalized_m_result.istd_resp_ratio

    return analyzes


def _remove_negative_values(analyzes: List[Analysis]) -> List[Analysis]:
    # TODO: I'm not sure this is pertinent
    for analysis in analyzes:
        for molecule_result in analysis.results:
            for m_result in molecule_result.m_results:
                if m_result.istd_resp_ratio < 0:
                    m_result.istd_resp_ratio = 0

    return analyzes
