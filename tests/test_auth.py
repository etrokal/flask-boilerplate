from flask.testing import FlaskClient
import pytest


def test_should_show_register_form(client: FlaskClient):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b'<form action="" method="post">' in response.data


@pytest.mark.parametrize(('username', 'email', 'password', 'password_confirmation', 'message'), [
    ('test', '', 'password', 'password', b'required'),
    ('test', 'test', 'password', 'password', b'invalid'),
    ('test', 'email@example', 'password', 'password', b'invalid'),
])
def test_register_validation(client: FlaskClient, username, email, password, password_confirmation, message):
    response = client.post("/auth/register", data={'username': username, 'email': email,
                           'password': password, 'password_confirmation': password_confirmation, })
    assert message in response.data
