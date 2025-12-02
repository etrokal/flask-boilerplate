from flask import Flask, session
from flask.testing import FlaskClient
import pytest
from sqlalchemy import select

from app.blueprints.auth import routes
from app.models.db import get_session
from app.models.user import User
from tests.conftest import AuthActions


def test_should_show_register_form(client: FlaskClient):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b'<form action="" method="post">' in response.data


@pytest.mark.parametrize(
    ('username', 'email', 'password', 'password_confirmation', 'message'),
    [
        ('test', '', 'password', 'password', b'This field is required.'),
        ('test', 'test', 'password', 'password', b'invalid'),
        ('test', 'email@example', 'password', 'password', b'invalid'),
        ('test', 'email@example.com', 'password', 'pa', b'equal'),
        ('', 'email@example.com', 'password',
         'password', b'This field is required.'),
        (('a' * 300), 'email@example.com', 'password', 'password', b'longer'),
        ('test1', 'email@example.com', 'password', 'password', b'exists'),
        ('test', 'mail1@example.com', 'password', 'password', b'exists'),
    ])
def test_register_validation(client: FlaskClient, username, email, password, password_confirmation, message):
    response = client.post("/auth/register", data={'username': username, 'email': email,
                           'password': password, 'password_confirmation': password_confirmation, })
    assert response.status_code == 200
    assert message in response.data


@pytest.mark.parametrize(
    ('username', 'email', 'password', 'password_confirmation'),
    [
        ('test', 'email@example.com', 'password', 'password'),
    ])
def test_should_register_valid_data(app: Flask, username, email, password, password_confirmation, client: FlaskClient):
    class CalledStatus:
        STATUS = False

        @classmethod
        def call(cls):
            cls.STATUS = True

    def fake_send_email(user: User):
        CalledStatus.call()

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(routes, "send_confirmation_mail", fake_send_email)

    with app.app_context():
        users = User.query.all()
        count = len(users)

    response = client.post(
        "/auth/register",
        data={
            'username': username,
            'email': email,
            'password': password,
            'password_confirmation': password_confirmation
        }
    )

    with app.app_context():
        users = User.query.all()
        new_count = len(users)

    assert new_count == (count + 1)
    assert response.status_code == 302
    assert CalledStatus.STATUS  # mail was sent


def test_login(auth: AuthActions, client) -> None:
    with client:
        response = auth.login()
        assert response.status_code == 302
        user_id = session.get('_user_id')
        assert user_id is not None
        assert user_id == "test1"


def test_register_success_page(client):
    response = client.get('/auth/register_success')
    assert response.status_code == 200


def test_signing_and_validating_token(app: Flask, client: FlaskClient):
    email = 'email@email.com'
    with app.app_context():
        token = routes.generate_verification_token(email)
        result_email = routes.validate_token(token)
        assert email == result_email
