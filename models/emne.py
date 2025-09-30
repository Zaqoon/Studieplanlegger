from pydantic import BaseModel, model_validator
from .semester import Semester

class Emne(BaseModel):
    kode: str
    semester: Semester
    studiepoeng: int

    @model_validator(mode="after")
    def normaliser(cls, m: "Emne"):
        m.kode = m.kode.strip().upper()
        if m.studiepoeng <= 0:
            raise ValueError("Studiepoeng må være større enn 0.")
        return m
