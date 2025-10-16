from sqlalchemy.orm import Session
from app import models
from app.schemas import person_schemas

def person_create(session:Session,person:person_schemas.PersonCreate):
    db_person = models.Person(**person.model_dump())
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person

def person_update(session:Session,person_id:int,person_update:person_schemas.PersonUpdate):
    db_person = session.get(models.Person,person_id)

    if db_person is None:
        return None
    
    update_data = person_update.model_dump()
    for key,value in update_data.items():
        setattr(db_person,key,value)

    session.commit()
    session.refresh(db_person)
    return db_person

def person_delete(session:Session,person_id:int):
    db_person = session.get(models.Person,person_id)

    if db_person is None:
        return None
    
    session.delete(db_person)
    session.commit()
    return db_person

def get_people(session:Session):
    people = session.query(models.Person).all()
    return people

def get_person(session:Session,person_id:int):
    person = session.get(models.Person,person_id)
    return person