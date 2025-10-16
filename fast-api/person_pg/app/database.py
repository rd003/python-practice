import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL").strip()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# for testing the connection
# conn = engine.connect()
# print("====> Connected")
# conn.close()