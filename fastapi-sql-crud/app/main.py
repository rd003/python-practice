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
