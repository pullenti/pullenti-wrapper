
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.Morphology import Morphology
from pullenti.morph.Explanatory import Explanatory

from .utils import (
    assert_one_of,
    assert_not_empty
)


RU = 'RU'
UA = 'UA'
BY = 'BY'
EN = 'EN'
IT = 'IT'
KZ = 'KZ'

LANGS = {RU, UA, BY, EN, IT, KZ}
DEFAULT_LANGS = {RU, EN}


def langs_to_raw(langs):
    raw = MorphLang()
    for lang in langs:
        lang = getattr(MorphLang, lang)
        raw |= lang
    return raw


def raw_to_langs(raw):
    langs = str(raw)  # RU;EN
    langs = (
        langs.split(';')
        if langs
        else []
    )
    for lang in langs:
        assert_one_of(lang, LANGS)
    return set(langs)


def loaded_langs():
    raw = Morphology.get_loaded_languages()
    return raw_to_langs(raw)


def unload_langs(langs):
    raw = langs_to_raw(langs)
    Morphology.unload_languages(raw)
    Explanatory.unload_languages(raw)


def load_langs(langs):
    raw = langs_to_raw(langs)
    Morphology.load_languages(raw)
    Explanatory.load_languages(raw)


def set_langs(langs):
    langs = set(langs)
    assert_not_empty(langs)
    for lang in langs:
        assert_one_of(lang, LANGS)

    missing = loaded_langs() - langs
    unload_langs(missing)

    load_langs(langs)
