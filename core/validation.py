from typing import Dict, List, Tuple
from models.emne import Emne
from models.studieplan import Studieplan


class StudieplanValidator:
    @staticmethod
    def kan_legge_til_emne(emne: Emne, semester_nr: int, studieplan: Studieplan, 
                          alle_emner: Dict[str, Emne]) -> Tuple[bool, str]:
        
        if studieplan.har_emne(emne.emnekode):
            return False, "Emnet er allerede i studieplanen"
        
        if not StudieplanValidator._gyldig_semester_for_emne(emne, semester_nr):
            return False, f"{emne.semester.capitalize()}emner kan ikke legges til i semester {semester_nr}"
        
        # if not StudieplanValidator._har_plass_i_semester(semester_nr, studieplan, alle_emner):
        #     return False, f"Semester {semester_nr} har ikke plass til flere studiepoeng"
        
        return True, ""
    
    @staticmethod
    def _gyldig_semester_for_emne(emne: Emne, semester_nr: int) -> bool:
        høst_semestre = [1, 3, 5]
        vår_semestre = [2, 4, 6]
        
        if emne.semester == "høst" and semester_nr in høst_semestre:
            return True
        if emne.semester == "vår" and semester_nr in vår_semestre:
            return True
        return False
    
    @staticmethod
    def _har_plass_i_semester(semester_nr: int, studieplan: Studieplan, 
                             alle_emner: Dict[str, Emne]) -> bool:
        current_poeng = StudieplanValidator._beregn_studiepoeng_i_semester(
            semester_nr, studieplan, alle_emner)
        return current_poeng < 30
    
    @staticmethod
    def _beregn_studiepoeng_i_semester(semester_nr: int, studieplan: Studieplan, 
                                      alle_emner: Dict[str, Emne]) -> int:
        total_poeng = 0
        for emnekode in studieplan.semestre[semester_nr]:
            if emnekode in alle_emner:
                total_poeng += alle_emner[emnekode].studiepoeng
        return total_poeng
    
    @staticmethod
    def valider_studieplan(studieplan: Studieplan, alle_emner: Dict[str, Emne]) -> Tuple[bool, List[str]]:
        feil = []
        
        for semester_nr in range(1, 7):
            poeng = StudieplanValidator._beregn_studiepoeng_i_semester(
                semester_nr, studieplan, alle_emner)
            if poeng != 30:
                feil.append(f"Semester {semester_nr}: {poeng} studiepoeng (krever 30)")
        
        return len(feil) == 0, feil
