from typing import List, Dict, Tuple
from models.studieplan import Studieplan
from models.emne import Emne
from core.validation import StudieplanValidator

class StudieplanService:
    def __init__(self, emne_service):
        self.studieplan = Studieplan()
        self.emne_service = emne_service
    
    def legg_til_emne_i_semester(self, emnekode: str, semester_nr: int) -> Tuple[bool, str]:
        emne = self.emne_service.hent_emne(emnekode)
        if not emne:
            return False, "Emnet finnes ikke"
        
        kan_legge_til, feilmelding = StudieplanValidator.kan_legge_til_emne(
            emne, semester_nr, self.studieplan, self.emne_service.hent_alle_emner())
        
        if kan_legge_til:
            self.studieplan.legg_til_emne(semester_nr, emnekode)
            return True, "Emne lagt til i studieplanen"
        
        return False, feilmelding
    
    def fjern_emne_fra_semester(self, emnekode: str, semester_nr: int) -> bool:
        self.studieplan.fjern_emne(semester_nr, emnekode)
        return True
    
    def hent_studieplan_oversikt(self) -> List[str]:
        oversikt = []
        semester_navn = {1: "1. semester (Høst)", 2: "2. semester (Vår)", 
                        3: "3. semester (Høst)", 4: "4. semester (Vår)",
                        5: "5. semester (Høst)", 6: "6. semester (Vår)"}
        
        for semester_nr in range(1, 7):
            emner = self.studieplan.semestre[semester_nr]
            oversikt.append(f"\n{semester_navn[semester_nr]}:")
            
            if not emner:
                oversikt.append("  Ingen emner")
            else:
                total_poeng = 0
                for emnekode in emner:
                    emne = self.emne_service.hent_emne(emnekode)
                    if emne:
                        oversikt.append(f"  {emnekode}: {emne.studiepoeng}sp")
                        total_poeng += emne.studiepoeng
                oversikt.append(f"  Total: {total_poeng} studiepoeng")
        
        return oversikt
    
    def valider_studieplan(self) -> Tuple[bool, List[str]]:
        return StudieplanValidator.valider_studieplan(
            self.studieplan, self.emne_service.hent_alle_emner())
