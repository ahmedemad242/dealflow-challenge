"""Flask app initialization via factory pattern."""
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from dealflow.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask("flask-api-tutorial")
    app.config.from_object(get_config(config_name))

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
