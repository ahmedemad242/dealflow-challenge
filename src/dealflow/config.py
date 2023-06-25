"""Config settings for for development, testing and production environments."""
import os
from pathlib import Path


HERE = Path(__file__).parent
SQLITE_DEV = "sqlite:///" + str(HERE / "dealflow_dev.db")
SQLITE_TEST = "sqlite:///" + str(HERE / "dealflow_test.db")
SQLITE_PROD = "sqlite:///" + str(HERE / "dealflow_prod.db")


class Config:
    """Base configuration."""

    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False

    # API documentation
    APIFAIRY_TITLE = "dealflow API"
    APIFAIRY_VERSION = "1.0"
    APIFAIRY_UI = os.environ.get("DOCS_UI", "elements")
    APIFAIRY_TAGS = ["freelancers"]


class TestingConfig(Config):
    """Testing configuration."""

    SERVER_NAME = "localhost:5000"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)


class ProductionConfig(Config):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, DevelopmentConfig)
