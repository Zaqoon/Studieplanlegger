from pydantic import BaseModel, Field
from typing import List

class Semester(BaseModel):
    nummer: int = Field(..., description="Semester nummer, f.eks., 1 for første semester")
    emner: List[str] = Field(default=[], description="Liste over emner i semesteret")
