from app.language import Language
from app.extensions import __, language

import pytest


def test_instantiating_language_object():
    language = Language()
    assert type(language) is Language
    assert 'pt_br' in language.languages


def test_can_change_locale_to_pt_br():
    language = Language()
    language.set_locale('pt_br')


def test_can_get_a_pt_br_message():
    language = Language()
    language.set_locale('pt_br')
    assert language.get_message('hello_world') == "Olá, mundo!"


def test_can_get_currency():
    language = Language()
    language.set_locale('pt_br')
    print(language.languages)
    assert language.get_currency_symbol() == "R$"


def test_shortcut_function(app):
    with app.app_context():
        language.set_locale("pt_br")
        assert __('hello_world') == "Olá, mundo!"
