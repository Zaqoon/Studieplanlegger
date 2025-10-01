import json
from typing import Dict, Tuple
from models.emne import Emne
from models.studieplan import Studieplan


class FileRepository:
    @staticmethod
    def lagre_data(emner: Dict[str, Emne], studieplan: Studieplan, filnavn: str = "studiedata.json"):
        data = {
            "emner": {
                kode: {
                    "emnekode": emne.emnekode,
                    "semester": emne.semester,
                    "studiepoeng": emne.studiepoeng
                } for kode, emne in emner.items()
            },
            "studieplan": studieplan.semestre
        }
        
        try:
            with open(filnavn, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, f"Data lagret til {filnavn}"
        except Exception as e:
            return False, f"Feil ved lagring: {str(e)}"
    
    @staticmethod
    def les_data(filnavn: str = "studiedata.json") -> Tuple[bool, str, Dict[str, Emne], Studieplan]:
        try:
            with open(filnavn, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            emner = {}
            for kode, emne_data in data.get("emner", {}).items():
                emner[kode] = Emne(
                    emne_data["emnekode"],
                    emne_data["semester"],
                    emne_data["studiepoeng"]
                )
            
            studieplan = Studieplan()
            studieplan_data = data.get("studieplan", {})
            for semester_str, emner_liste in studieplan_data.items():
                semester_nr = int(semester_str)
                studieplan.semestre[semester_nr] = emner_liste
            
            return True, f"Data lest fra {filnavn}", emner, studieplan
        except FileNotFoundError:
            return False, f"Finner ikke filen {filnavn}", {}, Studieplan()
        except Exception as e:
            return False, f"Feil ved lesing: {str(e)}", {}, Studieplan()
