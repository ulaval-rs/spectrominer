from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from spectrominer.parser.molecule_results import MoleculeResults


@dataclass
class Analysis:
    index: int
    name: str
    date: Optional[datetime]

    results: List[MoleculeResults]

    def __lt__(self, other: 'Analysis') -> bool:
        return self.name < other.name

    def __getitem__(self, molecule_name: str) -> MoleculeResults:
        for molecule_result in self.results:
            if molecule_result.name == molecule_name:
                return molecule_result

        raise KeyError(molecule_name)
