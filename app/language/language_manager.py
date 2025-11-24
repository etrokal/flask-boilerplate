import json
from pathlib import Path
from typing import Any, Dict
from decouple import config


class Language:
    """class to deal with languages"""
    languages: Dict[str, Dict[str, Any]]
    default_locale: str
    locale: str

    def __init__(self) -> None:
        self.default_locale = self._get_config_default_locale()
        self.locale = self.default_locale

        self._load_languages()

    def _get_config_default_locale(self) -> str:
        """pega o locale padrão da config"""
        default = config("DEFAULT_LOCALE", default="en_us")
        return str(default) if default is not None else "en_us"

    def _load_languages(self):
        """Carrega todos os arquivos language/*.json"""
        self.languages = {}
        language_dir = Path(__file__).resolve().parent
        if not language_dir.is_dir():
            raise FileNotFoundError(f"Directory {language_dir} not found.")

        for file_path in language_dir.glob("*.json"):
            lang_code = file_path.stem
            with file_path.open("r", encoding="utf-8") as f:
                self.languages[lang_code] = json.load(f)

    def set_locale(self, language_code: str) -> None:
        """
            Sets the locale of the app, via language code.
            If language code not loaded from json files, raise `ValueError`
        """
        if language_code not in self.languages:
            raise ValueError(
                f"Language code '{language_code}' not found. Available: {list(self.languages.keys())}")
        self.locale = language_code

    def get_message(self, msg: str) -> str:
        """
            Returns the correspondent message from the selected locale.
            Returns the given message if not found.
        """
        current_messages: Dict[str, str] = self.languages[self.locale].get(
            "messages", {})

        if (self.locale == self.default_locale or msg not in current_messages):
            return msg

        return current_messages[msg]

    def get_currency_symbol(self):
        if self.locale == self.default_locale:
            return 'US$' #FIXME: Should be a config value

        if 'currency' not in self.languages[self.locale]:
            raise ValueError(
                f"Unnable to load the currency for language code {self.locale}")
        return self.languages[self.locale]["currency"]
