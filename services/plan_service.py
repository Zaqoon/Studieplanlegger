from typing import Tuple, List, Dict
from models.emne import Emne


class PlanService:
    def __init__(self):
        pass

    def legg_til_emne_i_semester(self, kode: str, semester_nr: int) -> Tuple[bool, str]:
        pass

    def fjern_emne_fra_semester(self, kode: str, semester_nr: int) -> Tuple[bool, str]:
        pass

    def liste_over_semester(self, semester_nr: int) -> List[Emne]:
        pass

    def skriv_ut_plan(self) -> Dict[int, List[Emne]]:
        pass

    def sjekk_gyldighet(self) -> Tuple[bool, Dict[int, int]]:
        pass
    