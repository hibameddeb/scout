from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from io import BytesIO
from openpyxl import Workbook

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inscription Scouts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/people", response_model=list[schemas.PersonOut])
def list_people(db: Session = Depends(get_db)):
    return db.query(models.Person).order_by(desc(models.Person.id)).all()


@app.post("/api/people", response_model=schemas.PersonOut, status_code=201)
def create_person(payload: schemas.PersonCreate, db: Session = Depends(get_db)):
    person = models.Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.delete("/api/people/{person_id}", status_code=204)
def delete_person(person_id: str, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person)
    db.commit()
    return None


@app.get("/api/export")
def export_excel(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Inscrits"

    headers = ["Nom", "Type", "Tel", "Age", "Pull", "Statut", "Paiement", "Montant", "CNSS", "Ichtirak"]
    ws.append(headers)

    for p in people:
        ws.append([
            p.nom, p.dalila, p.tel, p.age, p.taille, p.statut,
            p.paiement, p.montant if p.montant is not None else "-",
            p.cnss, p.ichtirak
        ])

    for col in ws.columns:
        length = max(len(str(c.value)) for c in col if c.value is not None) if col else 10
        ws.column_dimensions[col[0].column_letter].width = max(12, length + 2)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=inscriptions_scouts.xlsx"}
    )
