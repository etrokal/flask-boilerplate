from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models.user import User
from app.validators.unique import Unique
from app.extensions import __


class RegisterForm(FlaskForm):
    username = StringField(__('Username'), validators=[
                           DataRequired(), Length(max=80), Unique(model=User, field=User.username, message=__('This user already exists'))])
    email = EmailField(
        label=__('E-mail'), validators=[DataRequired(), Length(max=255), Email(), Unique(model=User, field=User.email, message=__('This e-mail already exists'))])
    password = PasswordField(label=__('Password'), validators=[
                             DataRequired(), Length(min=8),  EqualTo(fieldname='password_confirmation', message=__('Must be equal to Password Confirmation'))])
    password_confirmation = PasswordField(label=__('Password Confirmation'), validators=[
                                          DataRequired(),])


class LoginForm(FlaskForm):
    username = StringField(
        label=__('Username'), validators=[DataRequired()])
    password = PasswordField(label=__('Password'), validators=[DataRequired()])
