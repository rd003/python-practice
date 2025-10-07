# Tutorial

## folder structure

```txt
fastapi-sql-crud/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── database.py       # Database connection and setup
│   ├── models.py         # SQLModel models
│   ├── schemas.py        # Pydantic schemas for validation
│   └── routers/
│       ├── __init__.py
│       └── person.py     # Person CRUD endpoints
├── person.db           # SQLite database (auto-created)
└── requirements.txt      # Python dependencies
```

**Note:** __init__.py indicates that app is a module. It will create a `app` module. You can import any file from it (eg. `from app.models import Person`)

## If you are not building the project and directly using my project

- Open the project in terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Note:** With `venv` (virtual environment), python packages are only going to install in the project level. If you don't use it, then dependencies will be installed globally

## If you are manually building the project

## Create virtual environment and install packages

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlmodel
```

- uvicorn is a server
- sqlmodel is an ORM (object relational mapper). It is needed to talk with database

## requirements.txt file

Create the `requirements.txt` file, so that we know the required packages in the future. This file keeps the track of all the required dependencies

```bash
    pip freeze > requirements.txt
```

In future, if you want to install all the dependencies, just run:

```bash
pip install -r requirements.txt
```

## Creating files

```bash
cd app
touch __init__.py main.py database.py models.py schemas.py crud.py utils.py

mkdir routers
touch routers/person.py routers/__init__.py
```

## database.py

```py
# app/database.py
from sqlmodel import SQLModel,create_engine,Session

DATABASE_URL = "sqlite:///./person.db"

engine = create_engine(DATABASE_URL,echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

## models.py

```py
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, max_length=30)
    last_name: str = Field(nullable=False, max_length=30)
    age: int = Field(nullable=False, gt=0, lt=150)
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
```

## schemas.py

```py
# app/schemas.py
# pydantic models for validation

# app/schemas.py
from pydantic import BaseModel, constr, Field
from datetime import datetime

# Shared validation logic
NameStr = constr(strip_whitespace=True, min_length=1, max_length=30)

class PersonBase(BaseModel):
    first_name: NameStr
    last_name: NameStr
    age: int = Field(gt=0)

class PersonCreate(PersonBase):
    pass  # same fields as base

class PersonRead(PersonBase):
    id: int
    created: datetime

    class Config:
        from_attributes = True  # needed for SQLModel → Pydantic

class PersonUpdate(BaseModel):
    first_name: NameStr | None = None
    last_name: NameStr | None = None
    age: int | None = Field(default=None, gt=0)
```

## crud.py

```py
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
```

## person.py

```py
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
```

## main.py

```py
# app/main.py
from fastapi import FastAPI
from .database import init_db
from .routers import person

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI + SQLModel CRUD Example")

    # Initialize DB
    init_db()

    # Routers
    app.include_router(person.router)

    return app

app = create_app()
```

## Run the application

Visit the root directory, if you are not there and run `uvicorn app.main:app --reload`

Open `http://127.0.0.1:8000/docs` in the browser, which will open the swagger docs.