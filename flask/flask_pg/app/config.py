import os
import urllib.parse

user = os.getenv("DB_USER", "postgres")
password = urllib.parse.quote_plus(os.getenv("DB_PASS", "p@55w0rd"))
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
dbname = os.getenv("DB_NAME", "books_db")

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False    