import os
import tempfile

from flask import Flask
from flask.testing import FlaskCliRunner, FlaskClient
from flask_sqlalchemy import SQLAlchemy
import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.models import db
from flask_migrate import upgrade, downgrade

from app.language.language_manager import Language
from app.models.user import User


# with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
#     _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://postgres:postgres@localhost:5432/flask_test",
        "SECRET_KEY": "asdfghdgjkhjlkgjhfdsaAFGHJKLL6Y5TEWRSF",
        "LOCALE": "en_us",
        "DEFAULT_LOCALE": "en_us",
        "WTF_CSRF_ENABLED": False,  # disable csrf for testing
        "SERVER_NAME": 'localhost',
        "APPLICATION_ROOT":  '/',
        "PREFERRED_URL_SCHEME": 'http'
    })

    with app.app_context():
        downgrade(revision="base")
        upgrade()
        seed_test_db(db)

    yield app

    with app.app_context():
        downgrade(revision="base")

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test1', password='password'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def language():
    return Language("en_us", "en_us")


@pytest.fixture
def auth(client):
    return AuthActions(client)


def seed_test_db(db: SQLAlchemy):
    user = User(username='test1', email='mail1@example.com',
                password=generate_password_hash('password'), active=True)
    db.session.add(instance=user)
    db.session.commit()
