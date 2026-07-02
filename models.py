import uuid
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Person(Base):
    __tablename__ = "people"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    dalila: Mapped[str] = mapped_column(String(20), nullable=False)   # Mourchida, Jawala, Kachef, Dalila
    tel: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    taille: Mapped[str] = mapped_column(String(5), nullable=False)    # XS..XXL
    statut: Mapped[str] = mapped_column(String(10), nullable=False)   # Jdid, 9dim
    paiement: Mapped[str] = mapped_column(String(10), nullable=False) # Total, Avance
    montant: Mapped[float | None] = mapped_column(Float, nullable=True)
    cnss: Mapped[str] = mapped_column(String(5), nullable=False)      # Oui, Non
    ichtirak: Mapped[str] = mapped_column(String(15), nullable=False) # Khales, Non paye
