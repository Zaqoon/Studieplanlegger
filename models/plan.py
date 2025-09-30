from typing import Dict, List
from pydantic import BaseModel, model_validator

class Plan(BaseModel):
    sem: Dict[int, List[str]]

    @model_validator(mode="before")
    def koercer_nokler(cls, v):
        d = v.get("sem", v)
        if isinstance(d, dict):
            ny = {}
            for k, val in d.items():
                if isinstance(k, str) and k.isdigit():
                    ny[int(k)] = list(val)
                elif isinstance(k, int):
                    ny[int(k)] = list(val)
            return {"sem": ny}
        return v

    @model_validator(mode="after")
    def normaliser(cls, m: "Plan"):
        for i in range(1, 7):
            m.sem.setdefault(i, [])
        ugyldige = [k for k in m.sem.keys() if k not in range(1, 7)]
        if ugyldige:
            raise ValueError("Ugyldige semesternøkler.")
        m.sem = {i: [k.strip().upper() for k in m.sem[i]] for i in range(1, 7)}
        return m
