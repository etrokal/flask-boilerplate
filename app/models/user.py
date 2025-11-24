from typing import override
from flask import g
from flask_login import UserMixin
from .base import BaseModel
from .. import db


class User(BaseModel, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_change_token = db.Column(db.String)
    email_confirmation_token = db.Column(db.String)
    active = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return self.username
