

def assert_not_empty(item):
    if len(item) == 0:
        raise ValueError('expected not empty')


def assert_one_of(item, items):
    if item not in items:
        raise ValueError('{item!r} not in {items!r}'.format(
            item=item,
            items=items
        ))
