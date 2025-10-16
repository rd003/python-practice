from fastapi import FastAPI
from app.routers import people
from app.database import engine, Base


# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Person api",description="CRUD Sample",version="1.0.0")

app.include_router(people.router)

