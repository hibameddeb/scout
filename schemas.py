from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, field_validator


class PersonBase(BaseModel):
    nom: str
    dalila: Literal["Mourchida", "Jawala", "Kachef", "Dalila"]
    tel: str
    age: int
    taille: Literal["XS", "S", "M", "L", "XL", "XXL"]
    statut: Literal["Jdid", "9dim"]
    paiement: Literal["Total", "Avance"]
    montant: Optional[float] = None
    cnss: Literal["Oui", "Non"]
    ichtirak: Literal["Khales", "Non paye"]

    @field_validator("montant")
    @classmethod
    def montant_required_if_avance(cls, v, info):
        paiement = info.data.get("paiement")
        if paiement == "Avance" and (v is None or v < 0):
            raise ValueError("montant is required and must be >= 0 when paiement is 'Avance'")
        return v


class PersonCreate(PersonBase):
    pass


class PersonOut(PersonBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
