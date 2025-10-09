# app/crud.py

from typing import Optional
from sqlmodel import Session, select
from app.models import Person
from app.schemas import PersonCreate, PersonUpdate

def create_person(session:Session,person:PersonCreate) -> Person:
    db_person = Person(**person.model_dump())  # dumping data from person to db_person, because they have different type
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person

def get_persons(session:Session):
    return session.exec(select(Person)).all()

def get_person(session:Session, id:int) -> Optional[Person]:
    return session.get(Person,id)
    
def update_person(session:Session,id:int,person_to_update:PersonUpdate) -> Optional[Person]:
   db_person = session.get(Person,id)
   if not db_person:
       return None
   update_data = person_to_update.model_dump(exclude_unset=True)

   for key,value in update_data.items():
       setattr(db_person,key,value)

   session.add(db_person)
   session.commit()
   session.refresh(db_person)
   return db_person

def delete_person(session:Session,id:int)->bool:
    db_person = session.get(Person,id)
    if not db_person:
        return False 
    session.delete(db_person)
    session.commit()
    return True   