from flask import Flask
from app.extensions import db, migrate
from config import Config  # This pulls in .env settings

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config from .env via config.py

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # Must come after db.init_app()

    # Register Blueprints
    from app.routes.user import user_bp
    from app.routes.supplier import supplier_bp

    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(supplier_bp, url_prefix="/supplier")

    return app
