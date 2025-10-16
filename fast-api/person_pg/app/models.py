from sqlalchemy import Column,Integer,String
from app.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(30),nullable=False)
    last_name = Column(String(30),nullable=False)