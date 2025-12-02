from flask import Flask
from app.models import User
import flask_login

login_manager = flask_login.LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter(User.username == user_id)
    if user is None:
        return

    return user


def init_app(app: Flask):
    login_manager.init_app(app)
