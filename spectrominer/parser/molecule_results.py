from dataclasses import dataclass
from typing import List


@dataclass
class MResult:
    m_number: int

    retention_time: float
    area: float
    istd_resp_ratio: float

    def __lt__(self, other: 'MResult') -> bool:
        return self.m_number < other.m_number


@dataclass
class MoleculeResults:
    name: str

    m_results: List[MResult]

    def __lt__(self, other: 'MoleculeResults') -> bool:
        return self.name < other.name
