from ctypes import ArgumentError
import glob
from typing import Any
from flask import g, json
from decouple import config


class Language:
    """class to deal with languages"""
    languages: dict[str, dict[str, Any]]

    def __init__(self) -> None:
        language_list = glob.glob("language/*.json")
        for lang in language_list:
            filename = lang.split('\\')
            lang_code = filename[1].split('.')[0]
            with open(lang, 'r', encoding='utf8') as file:
                self.languages[lang_code] = json.loads(file.read())

        self.default_locale = config("DEFAULT_LOCALE", default="en")

    def set_locale(self, language_code: str) -> None:
        """
            Sets the locale of the app, via language code.
            If language code not loaded from json files, raise `ArgumentError`
        """
        if language_code in self.languages:
            self.locale = language_code
        else:
            raise ArgumentError("Language code not found in language files.")

    def get_message(self, msg: str) -> str:
        """
            Returns the correspondent message from the selected locale.
            Returns the given message if not found.
        """
        if self.locale == self.default_locale or msg not in self.languages[self.locale]["messages"]:
            return msg

        return self.languages[self.locale]["messages"][msg]


def init_language_object() -> None:
    if 'language' not in g:
        g.language = Language()


def get_language_object() -> type[Language]:
    if 'language' not in g:
        raise Exception("Language object not initialized.")

    assert g.language is Language
    return g.language


def __(message: str) -> str:
    if 'language' not in g:
        raise Exception("Language object not initialized.")
    return g.language.get_message(message)
