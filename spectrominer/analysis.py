from dataclasses import dataclass
from datetime import datetime


@dataclass
class Analysis:
    index: int
    name: str
    date: datetime
