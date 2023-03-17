from distutils.util import strtobool
from os import environ

from app.enums.environment import Environment


class Config(object):
    DEBUG = False
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    ERROR_MESSAGE_KEY = environ.get("ERROR_MESSAGE_KEY", "message")

    JWT_AUTH_URL_RULE = environ.get("JWT_AUTH_URL_RULE")
    JWT_AUTH_USERNAME_KEY = environ.get("JWT_AUTH_USERNAME_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(environ.get("JWT_ACCESS_TOKEN_EXPIRES", 1800))
    JWT_REFRESH_TOKEN_EXPIRES = int(environ.get("JWT_REFRESH_TOKEN_EXPIRES", 259200))
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_ERROR_MESSAGE_KEY = ERROR_MESSAGE_KEY

    LOG_TYPE = environ.get("LOG_TYPE", "stream")
    LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    ENVIRONMENT = Environment.development
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = strtobool(environ.get("SQLALCHEMY_ECHO", "true"))


class ProductionConfig(Config):
    ENVIRONMENT = Environment.production
    DEBUG = False
    SQLALCHEMY_ECHO = strtobool(environ.get("SQLALCHEMY_ECHO", "false"))


CONFIGS = [DevelopmentConfig, ProductionConfig]
