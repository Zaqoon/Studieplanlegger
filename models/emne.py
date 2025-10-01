from dataclasses import dataclass
from typing import Literal


@dataclass
class Emne:
    emnekode: str
    semester: Literal["høst", "vår"]
    studiepoeng: int
    
    def __post_init__(self):
        if self.studiepoeng <= 0:
            raise ValueError("Studiepoeng må være større enn 0")
        if self.semester not in ["høst", "vår"]:
            raise ValueError("Semester må være 'høst' eller 'vår'")
            