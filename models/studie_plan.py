from pydantic import BaseModel, Field
from typing import Dict
from models.semester import Semester


class StudiePlan(BaseModel):
    semester: Dict[int, Semester] = Field(..., description="Dictionary som mapper semester nummer til Semester objekter")
