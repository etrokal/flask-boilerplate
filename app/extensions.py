

from typing import Any, Callable, override
from flask import current_app, has_app_context
from werkzeug.local import LocalProxy
from .language import Language


def _get_language() -> Language:
    try:
        return current_app.extensions['language']
    except (AttributeError, RuntimeError, KeyError):
        raise RuntimeError("Language extension not initialized")


language: LocalProxy[Language] = LocalProxy(_get_language)


class LazyString():
    """
    Class to translate strings lazily. 
    The translated message is only checked when converting to string, instead of on intantiation
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        if not has_app_context():
            return self.msg

        try:
            language = current_app.extensions['language']
            return language.get_message(self.msg)
        except Exception:
            return self.msg

    def __json__(self, app=None) -> str:
        """
        Custom method for JSON serialization (used by Flask's JSONProvider).
        Returns the object's string representation.
        """
        return str(self)

    def __html__(self) -> str:
        """
        Returns the full translated string for rendering.
        """
        return str(self)

    def __repr__(self):
        return f"<LazyString '{self.msg}'>"

    def __mod__(self, other):
        return str(self) % other

    def __add__(self, other):
        return str(self) + str(other)


def _translate(msg: str) -> LazyString:
    return LazyString(msg)


__ = LocalProxy(lambda: _translate)
