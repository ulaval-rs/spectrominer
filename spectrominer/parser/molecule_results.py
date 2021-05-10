from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MResult:
    m_number: int

    retention_time: Optional[float]
    area: Optional[float]
    istd_resp_ratio: float

    def __lt__(self, other: 'MResult') -> bool:
        return self.m_number < other.m_number


@dataclass
class MoleculeResults:
    name: str

    m_results: List[MResult]

    def __lt__(self, other: 'MoleculeResults') -> bool:
        return self.name < other.name

    def __getitem__(self, m_number: int) -> MResult:
        for m_result in self.m_results:
            if m_result.m_number == m_number:
                return m_result

        raise KeyError(f'M_number {m_number} not found')
