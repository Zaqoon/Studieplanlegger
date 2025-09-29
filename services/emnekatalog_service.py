from typing import List, Tuple
from models.emne import Emne
from models.semester import Semester


class EmneKatalogService:
    def __init__(self):
        pass

    def opprett_emne(self, kode: str, semester: str, studiepoeng: int):
        pass

    def hent_emne(self, kode: str) -> Emne | None:
        pass

    def alle_emner(self) -> List[Emne]:
        pass

    def slett_emne(self, kode: str) -> Tuple[bool, str]:
        pass
