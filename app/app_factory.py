from math import log
import os
from typing import Any, Mapping

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from decouple import config

from app import language
from app.language.language_manager import Language
from .config import Config
from app.blueprints.auth import login_manager
from app.lib import mail

from app.models import db, migrate


# TODO: Add security to the app
# TODO: Create command to generate secret key


def create_app(test_config:  Mapping[str, Any] | None = None) -> Flask:

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register DB
    db.init_app(app)
    migrate.init_app(app, db)       # This is the key line for Flask-Migrate

    # Register login manager
    login_manager.init_app(app=app)

    # Register flask-mail
    mail.init_app(app)

    # Register extensions
    app.extensions['language'] = Language(
        app.config["DEFAULT_LOCALE"], app.config["LOCALE"])

    register_context_processors(app)
    register_routes(app)

    return app


def register_context_processors(app: Flask):
    @app.context_processor
    def inject_translation_helper():
        from app.extensions import __
        return dict(__=__)


def register_routes(app: Flask):
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # auth
    from app.blueprints import auth
    app.register_blueprint(auth.bp)

    # home
    from app.blueprints import home
    app.register_blueprint(home.bp, )
    app.add_url_rule('/', endpoint='home.index')
