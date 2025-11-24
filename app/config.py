import os
import secrets
from decouple import config


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False)
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": config("SQLALCHEMY_ENG_OPT_POOL_PRE_PING", True)
    }
    SECRET_KEY = config('SECRET_KEY')
    SECURITY_PASSWORD_SALT = config(
        "SECURITY_PASSWORD_SALT", secrets.SystemRandom().getrandbits(128))
    REMEMBER_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SAMESITE = "strict"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
