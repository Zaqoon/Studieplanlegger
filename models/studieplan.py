from typing import List, Dict


class Studieplan:
    def __init__(self):
        self.semestre: Dict[int, List[str]] = {
            1: [], 2: [], 3: [], 4: [], 5: [], 6: []
        }
    
    def legg_til_emne(self, semester_nr: int, emnekode: str):
        if semester_nr not in self.semestre:
            raise ValueError("Ugyldig semester nummer")
        self.semestre[semester_nr].append(emnekode)
    
    def fjern_emne(self, semester_nr: int, emnekode: str):
        if semester_nr in self.semestre and emnekode in self.semestre[semester_nr]:
            self.semestre[semester_nr].remove(emnekode)
    
    def har_emne(self, emnekode: str) -> bool:
        for emner in self.semestre.values():
            if emnekode in emner:
                return True
        return False
