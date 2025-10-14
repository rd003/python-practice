# Tutorial

## Packages

```sh
pip install Flask psycopg2-binary Flask-SQLAlchemy Flask-Migrate
```

## Migration

```bash
flask db init
flask db migrate -m "Initial tables"
flask db upgrade
```