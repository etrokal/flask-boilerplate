import dbm
from typing import Any
from flask import Flask, g

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .base import BaseModel


# This file makes models a package and re-exports everything cleanly
from .user import User

# Optional: expose db here too if you like the shortcut
from .. import db   # re-export db from the parent package

__all__ = ['db', 'BaseModel', 'User']
