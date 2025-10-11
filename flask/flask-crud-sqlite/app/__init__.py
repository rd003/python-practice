from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from .routes.people_routes import people_bp
    app.register_blueprint(people_bp,url_prefix='/api/people')

    from .errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app    