from pydantic import BaseModel,Field

class PersonCreate(BaseModel):
    first_name:str = Field(...,max_length=30)
    last_name:str = Field(...,max_length=30)

class PersonUpdate(BaseModel):
    first_name:str = Field(...,max_length=30)
    last_name:str = Field(...,max_length=30)

class PersonResponse(BaseModel):
    id:int
    first_name:str
    last_name:str

    class Config:
        from_attributes = True
