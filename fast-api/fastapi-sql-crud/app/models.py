from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, max_length=30)
    last_name: str = Field(nullable=False, max_length=30)
    age: int = Field(nullable=False, gt=0, lt=150)
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
