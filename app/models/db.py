# Create the instances at module level (not yet bound to app)
from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


db = SQLAlchemy()
migrate = Migrate()


def get_session() -> Session:
    return current_app.extensions['sqlalchemy'].session
