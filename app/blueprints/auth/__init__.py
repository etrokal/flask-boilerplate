from decouple import config
from flask import Blueprint, Response, abort, render_template, request
from werkzeug.security import generate_password_hash

from app.blueprints.auth.form import RegisterForm
from app.models.user import User


from ... import db
from ... import models

import flask_login

login_manager = flask_login.LoginManager()

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@login_manager.user_loader
def user_loader(user_id):
    user = models.User.query.filter(User.username == user_id)
    if user is None:
        return

    return user


def init_app(app):
    login_manager.init_app(app)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    open_register = config("REGISTRATION_OPEN", default=True)
    if not open_register:
        abort(404)

    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        assert form.password.data is not None
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()

    return render_template('auth/register.jinja')


