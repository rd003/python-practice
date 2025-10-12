import os

# Path to repository root (parent of app/)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    # Default to a sqlite file in the repository root
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'people_db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
