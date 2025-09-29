from pydantic import BaseModel, Field


class Emne(BaseModel):
    kode: str = Field(..., description="Emnekode, f.eks., 'DAT'")
    term: str = Field(..., description="Term, f.eks., 'Høst' or 'Vår'")
    studie_poeng: int = Field(..., description="Antall studiepoeng for emnet")
    tittel: str = Field(..., description="Tittel på emnet")
