from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)

    from .routes import book_bp 
    app.register_blueprint(book_bp)

    from .error_handlers import register_error_handlers
    register_error_handlers(app)

    return app