from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models.user import User
from app.validators.unique import Unique


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Unique(model=User, field=User.username)])
    email = EmailField(
        label='E-mail', validators=[DataRequired(), Email(), Unique(model=User, field=User.email)])
    password = PasswordField(label='Password', validators=[
                             DataRequired(), Length(min=8)])
    password_confirmation = PasswordField(label='Password Confirmation', validators=[
                                          DataRequired(), EqualTo(fieldname='password')])


class LoginForm(FlaskForm):
    username = StringField(
        label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
