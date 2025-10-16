# tutorial

## packages

with pip:

```sh
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-dotenv
```

with uv:

```sh
uv pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-dotenv
```

## .env

env:

```env
DATABASE_URL=postgresql://postgres:p%4055w0rd@localhost:5432/person_db
```

## database.py

```py
# person_pg/app/database.py
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
```

### Initialize migration

Make sure, you are at the root directory not in the `app` directory.


```sh
alembic init alembic
```

### edit person_pg/alembic/env.py

add following content

```py
# person_pg/alembic/env.py
config = context.config

from app.database import Base,DATABASE_URL
from app.models import Person

url_str = DATABASE_URL.replace('%', '%%')

config.set_main_option('sqlalchemy.url',url_str)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  
```

Note: My password is `p@55w0rd`, which is encoded to `p%4055w0rd`

### create migration:

```sh
alembic revision --autogenerate -m "Create people table"    
```

apply to database:

```sh
alembic upgrade head
```

## to run 

```sh
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to open swagger ui