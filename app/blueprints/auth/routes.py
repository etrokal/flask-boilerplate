from decouple import config
from flask import Blueprint, Response, abort, redirect, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.blueprints.auth.form import LoginForm, RegisterForm
from app.models.user import User
from app.extensions import __


from ... import db
from ... import models

import flask_login


bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')
login_manager = flask_login.LoginManager()


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
        return redirect(url_for('auth.login'))

    print(form.errors)
    return render_template('auth/register.jinja', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        assert username is not None
        assert password is not None

        user = models.User.query.filter(
            models.User.username == username).first()

        if user is None or not check_password_hash(user.password, password):
            flash(__("Wrong username or password"), )
        else:
            flask_login.login_user(user)
            flash(__('Login successful!'), category="success")
            return redirect(location=url_for('home.index'))

    return render_template("auth/login.jinja", form=form)
