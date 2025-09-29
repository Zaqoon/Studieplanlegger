from typing import List, Tuple

from models.emne import Emne
from models.semester import Semester
from models.studie_plan import StudiePlan


class ValideringService:
    def __init__(self):
        pass

    def gyldig_semester_for_emne(self, semester_nr: int, emne: Emne) -> bool:
        pass

    def har_plass(self, semester: Semester, emne: Emne, katalog) -> bool:
        pass

    def sjekk_plass(self, studieplan: StudiePlan, katalog) -> Tuple[bool, List[str]]:
        pass
    