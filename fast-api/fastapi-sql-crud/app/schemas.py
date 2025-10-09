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
