
from pullenti.ner.ReferentToken import ReferentToken

from pullenti_client.result import (
    Span,
    Match,
    Result as Result_,
)

from .referent import convert_referents


class Result(Result_):
    raw = None


def get_match(token, referents):
    referent = referents.get(id(token.referent))
    if not referent:
        # Rare MAYBE TODO
        return

    start = token.begin_token
    stop = token.end_token
    span = Span(start.begin_char, stop.end_char + 1)
    children = list(get_matches(start, stop, referents))
    return Match(referent, span, children)


def get_matches(token, stop=None, referents=None):
    while token:
        if isinstance(token, ReferentToken):
            match = get_match(token, referents)
            if match:
                yield match
        if token == stop:
            break
        token = token.next0_


def convert_result(text, raw):
    referents = convert_referents(raw.entities)
    matches = list(get_matches(raw.first_token, referents=referents))
    result = Result(text, matches)
    result.raw = raw
    return result
