from datetime import datetime, timedelta, timezone
from typing import Dict
from decouple import config
from flask import Blueprint, Response, abort, current_app, redirect, render_template, request, template_rendered, url_for, flash
from flask_mail import Message
import jwt

from sqlalchemy.orm.session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers.response import Response

from app.blueprints.auth.form import LoginForm, RegisterForm
from app.lib import mail
from app.models.db import get_session
from app.models.user import User
from app.extensions import __
from app.blueprints.auth import routes

from sqlalchemy import select


import flask_login


bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    session = get_session()
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
        session.add(user)
        session.commit()
        send_confirmation_mail(user)  # TODO: change to use queue
        return redirect(url_for('auth.register_success'))

    return render_template('auth/register.jinja', form=form)


@bp.route('/email_confirmation_request')
def email_confirmation_request():
    return render_template('auth/email_confirmation_request')


@bp.route('/login', methods=['GET', 'POST'])
def login() -> Response | str:
    form = LoginForm()
    if form.validate_on_submit():
        session: Session = get_session()

        username: str | None = form.username.data
        password: str | None = form.password.data

        assert username is not None
        assert password is not None

        user = session.scalars(select(User).where(
            User.username == username)).first()

        if user is None or not check_password_hash(user.password, password):
            flash(__("Wrong username or password"), )
        else:
            if flask_login.login_user(user):
                flash(__('Login successful!'), category="success")
                return redirect(location=url_for('home.index'))
            else:
                flash(__('User disabled.'))

    return render_template("auth/login.jinja", form=form)


@bp.route('/register_success', methods=['GET'])
def register_success():
    return render_template('auth/register_success.jinja')


@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_user_email(token: str):
    session = get_session()
    verification_ok = False

    if not token:
        abort(404)

    try:
        user_id = validate_token(token)
        if user_id:
            user = session.scalars(select(User).where(
                User.username == user_id)).first()

            if not user:
                abort(404)

            user.active = True
            session.merge(user)
            session.commit()
            # flash(__('E-mail verified.'))
            verification_ok = True
            return redirect(url_for('login'))

    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidTokenError,  jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError, ValueError) as e:  # type: ignore
        flash(__('Your link is invalid or expired.'))
        verification_ok = False

    return render_template('auth/verify_user_email', show_validate_link=verification_ok)


# private


def send_confirmation_mail(user: User):
    msg: Message = create_mail_message(user)
    mail.send(msg)


def create_mail_message(user: User) -> Message:
    email = user.email
    username = user.username
    link = url_for('auth.verify_user_email',
                   token=generate_verification_token(email))
    sender: tuple[str, str] = (
        current_app.config.get('MAIL_DEFAULT_SENDER', ""),
        current_app.config.get('MAIL_USERNAME', "")
    )
    msg = Message(
        subject=__('Mail confirmation'),
        sender=sender,
        recipients=[email]
    )
    msg.body = render_template(
        'mail/mail_confirmation.jinja', username=username, link=link)

    return msg


def generate_verification_token(email) -> str:
    max_age = int(current_app.config.get('SIGNED_LINKS_MAX_AGE', '1200'))
    secret_key = str(current_app.config.get('SECRET_KEY'))
    payload = {
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=max_age)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def validate_token(token: str,) -> str:
    """
        :param token -> The signed token from the link
        :return The `user_id` contained in the token
        Throws: SignatureExpired, BadSignature if invalid
    """
    secret_key = str(current_app.config.get('SECRET_KEY'))
    payload = jwt.decode(token, secret_key, algorithms=[
                         'HS256'], options={'require': ['exp']})

    return str(payload['email'])
