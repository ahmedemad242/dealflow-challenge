"""Unit tests for environment config settings."""
import os

from dealflow import create_app
from dealflow.config import SQLITE_DEV, SQLITE_PROD, SQLITE_TEST


def test_config_development():
    app = create_app("development")
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL", SQLITE_DEV)


def test_config_testing():
    app = create_app("testing")
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == SQLITE_TEST


def test_config_production():
    app = create_app("production")
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv(
        "DATABASE_URL", SQLITE_PROD
    )
