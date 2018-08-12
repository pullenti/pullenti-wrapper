
from collections import OrderedDict


def assert_type(item, types):
    if not isinstance(item, types):
        if not isinstance(types, tuple):
            types = [types]
        raise TypeError('expected {types}, got {type}'.format(
            types=' or '.join(_.__name__ for _ in types),
            type=type(item).__name__
        ))


def assert_not_empty(item):
    if len(item) == 0:
        raise ValueError('expected not empty')


def assert_one_of(item, items):
    if item not in items:
        raise ValueError('{item!r} not in {items!r}'.format(
            item=item,
            items=items
        ))


def jsonify(record):
    data = OrderedDict()
    for key in record.__attributes__:
        value = getattr(record, key)
        if isinstance(value, list):
            value = [jsonify(_) for _ in value]
        elif isinstance(value, Record):
            value = value.as_json
        data[key] = value
    return data


class Record(object):
    __attributes__ = []

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and all(
                (getattr(self, _) == getattr(other, _))
                for _ in self.__attributes__
            )
        )

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return (getattr(self, _) for _ in self.__attributes__)

    def __hash__(self):
        return hash(tuple(self))

    @property
    def as_json(self):
        return jsonify(self)

    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            '{key}={value!r}'.format(
                key=_,
                value=getattr(self, _)
            )
            for _ in self.__attributes__
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            printer.text('{name}('.format(name=name))
            keys = self.__attributes__
            size = len(keys)
            if size:
                with printer.indent(4):
                    printer.break_()
                    for index, key in enumerate(keys):
                        printer.text(key + '=')
                        value = getattr(self, key)
                        printer.pretty(value)
                        if index < size - 1:
                            printer.text(',')
                            printer.break_()
                printer.break_()
            printer.text(')')
