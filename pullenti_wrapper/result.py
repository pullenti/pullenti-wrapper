
from pullenti.ner.ReferentToken import ReferentToken

from .utils import (
    Record,
    assert_type
)
from .referent import (
    convert_referents,
    Referent
)
from .graph import Graph


class Span(Record):
    __attributes__ = ['start', 'stop']

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class Match(Record):
    __attributes__ = ['referent', 'span', 'children']

    def __init__(self, referent, span, children):
        assert_type(referent, Referent)
        self.referent = referent
        assert_type(span, Span)
        self.span = span
        for child in children:
            assert_type(child, Match)
        self.children = children

    def walk(self):
        yield self
        for child in self.children:
            for item in child.walk():
                yield item


def get_match(token, referents):
    referent = referents[id(token.referent)]
    start = token.begin_token
    stop = token.end_token
    span = Span(start.begin_char, stop.end_char + 1)
    children = list(get_matches(start, stop, referents))
    return Match(referent, span, children)


def get_matches(token, stop=None, referents=None):
    while token:
        if isinstance(token, ReferentToken):
            yield get_match(token, referents)
        if token == stop:
            break
        token = token.next0_


def convert_result(text, raw):
    referents = convert_referents(raw.entities)
    matches = list(get_matches(raw.first_token, referents=referents))
    result = Result(text, matches)
    result.raw = raw
    return result


class Result(Record):
    __attributes__ = ['text', 'matches']
    raw = None

    def __init__(self, text, matches):
        self.text = text
        self.matches = matches

    def walk(self):
        for match in self.matches:
            for item in match.walk():
                yield item

    @property
    def graph(self):
        graph = Graph()
        for match in self.walk():
            graph.update(match.referent.graph)
        return graph
