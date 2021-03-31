from dataclasses import dataclass
from typing import List


@dataclass
class MResult:
    m_number: int

    retention_time: float
    area: float
    istd_resp_ratio: float


@dataclass
class MoleculeResults:
    name: str

    m_results: List[MResult]
