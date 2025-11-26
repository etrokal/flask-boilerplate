import os
import tempfile

from flask_sqlalchemy import SQLAlchemy
import pytest

from app import create_app, db
from flask_migrate import upgrade, downgrade

from app.language.language_manager import Language


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
        "DEFAULT_LOCALE": "en_us"

    })

    with app.app_context():
        # Insert database code
        upgrade()
        seed_test_db(db)

    yield app

    with app.app_context():
        downgrade()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# TODO: alter to use my authentication


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
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
    pass
