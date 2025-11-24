

from typing import Any, Callable
from flask import current_app
from werkzeug.local import LocalProxy
from .language import Language


def _get_language_object() -> Language:
    if 'language' not in current_app.extensions:
        from .language import Language
        current_app.extensions['language'] = Language()

    return current_app.extensions['language']


language: LocalProxy[Language] = LocalProxy(_get_language_object)


def _get_message_shortcut() -> Callable[..., str]:
    def __(msg: str) -> str:
        if 'language' not in current_app.extensions:
            raise ValueError(
                "Language extension must be loaded before using the shortcut")

        language = current_app.extensions['language']
        assert type(language) is Language
        return language.get_message(msg)

    if '__' not in current_app.extensions:
        current_app.extensions['__'] = __

    return current_app.extensions['__']


__: LocalProxy[Callable[..., str]] = LocalProxy(_get_message_shortcut)
