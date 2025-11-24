import os
from typing import Any, Mapping

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app import language
from app.language.language_manager import Language
from .config import Config

# Create the instances at module level (not yet bound to app)
db = SQLAlchemy()
migrate = Migrate()

# TODO: Add security to the app


def create_app(test_config:  Mapping[str, Any] | None = None) -> Flask:

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY=config('SECRET_KEY'),
    #     SQLALCHEMY_DATABASE_URI=config('SQLALCHEMY_DATABASE_URI'),
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
        # app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)          # This is the key line for Flask-Migrate

    # Initialize language
    if 'language' not in app.extensions:
        app.extensions['language'] = Language()

    # import extensions
    from . import extensions

    # a simple page that says hello

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')

    from . import models

    return app
