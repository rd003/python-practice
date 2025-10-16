from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.schemas import person_schemas
from sqlalchemy.orm import Session
from app.crud import person_crud

router = APIRouter(
    prefix="/api/people",
    tags=['people']
)

@router.get("/",response_model=List[person_schemas.PersonResponse])
def get_people(session:Session = Depends(get_db)):
    people = person_crud.get_people(session)
    return people

@router.get("/{person_id}",response_model=person_schemas.PersonResponse)
def get_person(person_id:int,session:Session = Depends(get_db)):
    person = person_crud.get_person(session,person_id)
    if person is None:
        raise HTTPException(status_code=404,detail="Person not found")
    return person

@router.post("/",response_model=person_schemas.PersonResponse,status_code=201)
def create_person(person_create:person_schemas.PersonCreate,session:Session = Depends(get_db)):
    created_person = person_crud.person_create(session,person_create)
    return created_person

@router.put("/{person_id}",response_model=person_schemas.PersonResponse)
def update_person(person_id:int,person_update:person_schemas.PersonUpdate,session:Session=Depends(get_db)):
    update_person = person_crud.person_update(session,person_id,person_update)
    if update_person is None:
        raise HTTPException(status_code=404,detail="Person not found")
    return update_person

@router.delete("/{person_id}",status_code=204)
def delete_person(person_id:int,session:Session=Depends(get_db)):
    deleted_person = person_crud.person_delete(session,person_id)
    if deleted_person is None:
        raise HTTPException(404,"Person does not found")