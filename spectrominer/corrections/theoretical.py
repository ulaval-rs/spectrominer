import copy
from typing import List

import numpy
import pandas

from spectrominer.corrections.util import sum_m_results
from spectrominer.errors import CorrectionMatrixNotFoundError
from spectrominer.parser.analysis import Analysis
from spectrominer.parser.molecule_results import MoleculeResults


def apply_theoretical_corrections(analyzes: List[Analysis]) -> List[Analysis]:
    raise NotImplementedError('Theoretical corrections have not yet been implemented')

    for analysis in analyzes:
        analysis.results = [
            _correct_molecule_results(molecule_results) for molecule_results in analysis.results
        ]

    return analyzes


def _correct_molecule_results(molecule_results: MoleculeResults) -> MoleculeResults:
    # TODO: remove background noise

    # Normalization
    sum_of_m_results = sum_m_results(molecule_results)
    for m_result in molecule_results.m_results:
        # To get relative proportion
        m_result.istd_resp_ratio = m_result.istd_resp_ratio / sum_of_m_results

    # Applying correction matrix (gives proportional distribution)
    correction_matrix = _find_correction_matrix(molecule_results.name)
    molecule_results = _apply_correction_matrix(correction_matrix, molecule_results)

    # TODO: validate what is happening here
    # Going back to absolute
    new_sum_of_m_results = sum_m_results(molecule_results)
    for m_result in molecule_results.m_results:
        # Proportional distribution
        m_result.istd_resp_ratio /= new_sum_of_m_results

        # To get relative ion amounts
        # cg102 = Myristic ratio
        # bg119 = Protein ratio
        # bg104 = sum(values [M+0, M+1, ..., M+N] without background noise)
        # bg123 = average(bg104 / (cg102 * bg119))
        # bg140 = bg104 / (cg102 * bg119)
        # bg157 = bg140 / bg123
        # istd = istd * bg157
        m_result.istd_resp_ratio *= sum_of_m_results

        # To get absolute proportion
        # istd = istd * bg140
        m_result.istd_resp_ratio *= 1

    return molecule_results


def _apply_correction_matrix(
        correction_matrix: List[List[float]],
        molecule_results: MoleculeResults) -> MoleculeResults:
    molecule_results_tmp = copy.deepcopy(molecule_results)
    nbr_of_M = len(molecule_results.m_results)

    for m_result in molecule_results.m_results:
        m_result.istd_resp_ratio = 0

        for i in range(nbr_of_M):
            if not pandas.isna(molecule_results_tmp.m_results[i].istd_resp_ratio):
                m_result.istd_resp_ratio += molecule_results_tmp.m_results[i].istd_resp_ratio * \
                                            correction_matrix[i][m_result.m_number]
    # Reapplying the nan
    for m_result, m_result_tmp in zip(molecule_results.m_results, molecule_results_tmp.m_results):
        if pandas.isna(m_result_tmp.istd_resp_ratio):
            m_result.istd_resp_ratio = numpy.NAN

    return molecule_results


def _find_correction_matrix(molecule_name: str) -> List[List[float]]:
    molecule_name = molecule_name.lower()

    if ('lactic' in molecule_name or
            'lactate' in molecule_name):
        return [
            [1.1714235469, 0, 0, 0],
            [-0.143275149, 1.1714235469, 0, 0],
            [-0.0357412341, -0.143275149, 1.1714235469, 0],
            [0.0070255799, -0.0357412341, -0.143275149, 1.1714235469],
        ]

    if 'pyruvate' in molecule_name:
        return [
            [1.1714235469, 0, 0, 0],
            [-0.143275149, 1.1714235469, 0, 0],
            [-0.0357412341, -0.143275149, 1.1714235469, 0],
            [0.0070255799, -0.0357412341, -0.143275149, 1.1714235469],
        ]

    if ('citric' in molecule_name or
            'isocitric' in molecule_name or
            'cis-aconitic' in molecule_name):
        return [
            [1.6132733631, 0, 0, 0, 0, 0, 0],
            [-0.6078551163, 1.6132733631, 0, 0, 0, 0, 0],
            [-0.0592516758, -0.6078551163, 1.6132733631, 0, 0, 0, 0],
            [0.0590988538, -0.0592516758, -0.6078551163, 1.6132733631, 0, 0, 0],
            [-0.002316818, 0.0590988538, -0.0592516758, -0.6078551163, 1.6132733631, 0, 0],
            [-0.0035026031, -0.002316818, 0.0590988538, -0.0592516758, -0.6078551163, 1.6132733631, 0],
            [0.0004322514, -0.0035026031, -0.002316818, 0.0590988538, -0.0592516758, -0.6078551163, 1.6132733631],
        ]

    if ('succinate' in molecule_name or
            'succinic' in molecule_name):
        return [
            [1.3557434196, 0, 0, 0, 0],
            [-0.3207934912, 1.3557434196, 0, 0, 0],
            [-0.059504915, -0.3207934912, 1.3557434196, 0, 0],
            [0.0245545182, -0.059504915, -0.3207934912, 1.3557434196, 0],
            [0.001190865, 0.0245545182, - 0.059504915, - 0.3207934912, 1.3557434196],
        ]

    if 'alanine' in molecule_name:
        return [
            [1.3398573874, 0, 0, 0],
            [-0.3066721581, 1.3398573874, 0, 0],
            [-0.0557821354, -0.3066721581, 1.3398573874, 0],
            [0.0225565166, -0.0557821354, -0.3066721581, 1.3398573874],
        ]

    if 'glycine' in molecule_name:
        return [
            [1.325123287, 0, 0],
            [-0.2885699855, 1.325123287, 0],
            [-0.0585357935, -0.2885699855, 1.325123287],
        ]

    if ('fumarate' in molecule_name or
            'fumaric' in molecule_name):
        return [
            [1.3553367271, 0, 0, 0, 0],
            [-0.3202905984, 1.3553367271, 0, 0, 0],
            [-0.0595832579, -0.3202905984, 1.3553367271, 0, 0],
            [0.0245292964, -0.0595832579, -0.3202905984, 1.3553367271, 0],
            [0.0011978717, 0.0245292964, -0.0595832579, -0.3202905984, 1.3553367271],
        ]

    if ('malate' in molecule_name or
            'malic' in molecule_name):
        return [
            [1.5750972072, 0, 0, 0, 0],
            [-0.558799321, 1.5750972072, 0, 0, 0],
            [-0.0674792181, -0.558799321, 1.5750972072, 0, 0],
            [0.0552031383, -0.0674792181, -0.558799321, 1.5750972072, 0],
            [-0.0011440246, 0.0552031383, -0.0674792181, -0.558799321, 1.5750972072],
        ]

    if 'glutamine' in molecule_name:
        return [
            [1.5970886086, 0, 0, 0, 0, 0],
            [-0.5954145577, 1.5970886086, 0, 0, 0, 0],
            [-0.0512602506, -0.5954145577, 1.5970886086, 0, 0, 0],
            [0.0546212453, -0.0512602506, -0.5954145577, 1.5970886086, 0, 0],
            [-0.0024142761, 0.0546212453, -0.0512602506, -0.5954145577, 1.5970886086, 0],
            [-0.003126781, -0.0024142761, 0.0546212453, -0.0512602506, -0.5954145577, 1.5970886086],
        ]

    if ('glutamate' in molecule_name or
            'glutamic' in molecule_name):
        return [
            [1.5948481217, 0, 0, 0, 0, 0],
            [-0.5890568127, 1.5948481217, 0, 0, 0, 0],
            [-0.0565258057, -0.5890568127, 1.5948481217, 0, 0, 0],
            [0.0555795819, -0.0565258057, -0.5890568127, 1.5948481217, 0, 0],
            [-0.0021062806, 0.0555795819, -0.0565258057, -0.5890568127, 1.5948481217, 0],
            [-0.0032450442, -0.0021062806, 0.0555795819, -0.0565258057, -0.5890568127, 1.5948481217],
        ]

    if 'serine' in molecule_name:
        return [
            [1.5566408794, 0, 0, 0],
            [-0.5402125396, 1.5566408794, 0, 0],
            [-0.0645959281, -0.5402125396, 1.5566408794, 0],
            [0.0518300392, -0.0645959281, -0.5402125396, 1.5566408794],
        ]

    if ('aspartate' in molecule_name or
            'aspartic' in molecule_name):
        return [
            [1.5773099474, 0, 0, 0, 0],
            [-0.565046072, 1.5773099474, 0, 0, 0],
            [-0.0623748675, -0.565046072, 1.5773099474, 0, 0],
            [0.0543450644, -0.0623748675, -0.565046072, 1.5773099474, 0],
            [-0.0014722851, 0.0543450644, -0.0623748675, -0.565046072, 1.5773099474],
        ]

    if 'asparagine' in molecule_name:
        return [
            [1.5795257961, 0, 0, 0, 0],
            [-0.5713092714, 1.5795257961, 0, 0, 0],
            [-0.0572371033, -0.5713092714, 1.5795257961, 0, 0],
            [0.0534551329, -0.0572371033, -0.5713092714, 1.5795257961, 0],
            [-0.0017874121, 0.0534551329, -0.0572371033, -0.5713092714, 1.5795257961],
        ]

    raise CorrectionMatrixNotFoundError(f'No corrections found for {molecule_name}')

