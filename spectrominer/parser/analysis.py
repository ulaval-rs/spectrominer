from dataclasses import dataclass
from datetime import datetime
from typing import List

from spectrominer.parser.molecule_results import MoleculeResults


@dataclass
class Analysis:
    index: int
    name: str
    date: datetime

    results: List[MoleculeResults]
