from typing import Dict, List, Optional
from models.emne import Emne

class EmneService:
    def __init__(self):
        self.emner: Dict[str, Emne] = {}
    
    def opprett_emne(self, emnekode: str, semester: str, studiepoeng: int) -> bool:
        try:
            if emnekode in self.emner:
                return False
            
            emne = Emne(emnekode, semester, studiepoeng)
            self.emner[emnekode] = emne
            return True
        except ValueError:
            return False
    
    def hent_emne(self, emnekode: str) -> Optional[Emne]:
        return self.emner.get(emnekode)
    
    def hent_alle_emner(self) -> Dict[str, Emne]:
        return self.emner.copy()
    
    def slett_emne(self, emnekode: str) -> bool:
        if emnekode in self.emner:
            del self.emner[emnekode]
            return True
        return False
    
    def get_emner_list(self) -> List[str]:
        return [f"{kode}: {emne.semester}, {emne.studiepoeng}sp" 
                for kode, emne in self.emner.items()]
