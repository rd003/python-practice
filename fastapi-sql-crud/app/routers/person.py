# app/routers/person.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from .. import crud, schemas, database

router = APIRouter(prefix="/persons", tags=["persons"])

@router.post("/", response_model=schemas.PersonRead, status_code=201)
def create_person(person: schemas.PersonCreate, session: Session = Depends(database.get_session)):
    return crud.create_person(session, person)

@router.get("/", response_model=List[schemas.PersonRead])
def read_persons(session: Session = Depends(database.get_session)):
    return crud.get_persons(session)

@router.get("/{person_id}", response_model=schemas.PersonRead)
def read_person(person_id: int, session: Session = Depends(database.get_session)):
    db_person = crud.get_person(session, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.put("/{person_id}", response_model=schemas.PersonRead)
def update_person(person_id: int, updates: schemas.PersonUpdate, session: Session = Depends(database.get_session)):
    db_person = crud.update_person(session, person_id, updates)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/{person_id}", status_code=204)
def delete_person(person_id: int, session: Session = Depends(database.get_session)):
    success = crud.delete_person(session, person_id)
    if not success:
        raise HTTPException(status_code=404, detail="Person not found")
