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
    TEMPLATES_AUTO_RELOAD = config(
        "DEBUG", default=False, cast=bool)
    DEBUG = config(
        "DEBUG", default=False, cast=bool)
    LOCALE = config("LOCALE", default="en_us")
    DEFAULT_LOCALE = config("DEFAULT_LOCALE", default="en_us")
    SIGNED_LINKS_MAX_AGE = config(
        "SIGNED_LINKS_MAX_AGE", default="1200", cast=int)
    MAIL_SERVER = config("MAIL_SERVER")
    MAIL_PORT = config("MAIL_SMTP_PORT", default=587, cast=int)
    MAIL_USE_TLS = config("MAIL_USE_TLS", default=False, cast=bool)
    MAIL_USE_SSL = config("MAIL_USE_SSL", default=False, cast=bool)
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = config("MAIL_DEFAULT_SENDER", default="Flask App")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
