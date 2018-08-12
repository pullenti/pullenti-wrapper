
from subprocess import Popen, PIPE

from .utils import Record


BLUE = '#aec7e8'
ORANGE = '#ffbb78'
GREEN = '#dbdb8d'
RED = '#ff9896'
PURPLE = '#f7b6d2'
SILVER = '#eeeeee'
GRAY = 'gray'
DARKGRAY = '#888888'


def dot2svg(source):
    process = Popen(
        ['dot', '-T', 'svg'],
        stdin=PIPE, stdout=PIPE, stderr=PIPE
    )
    output, error = process.communicate(source.encode('utf8'))
    if process.returncode != 0:
        raise ValueError(error)
    return output.decode('utf8')


class style(Record):
    __attributes__ = ['attributes']

    def __init__(self, **attributes):
        self.attributes = attributes

    def quote(self, value):
        value = str(value)
        replace = {
            '"': r'\"',
            '\n': r'\n',
            '\r': r'\r'
        }
        for a, b in replace.items():
            value = value.replace(a, b)
        return '"' + value + '"'

    def __str__(self):
        return ', '.join(
            '{key}={value}'.format(
                key=key,
                value=self.quote(value)
            )
            for key, value in self.attributes.items()
        )


class Node(Record):
    __attributes__ = ['item', 'style']

    def __init__(self, item, style):
        self.item = item
        self.style = style

    def __hash__(self):
        return id(self.item)


class Edge(Record):
    __attributes__ = ['source', 'target', 'style']

    def __init__(self, source, target, style):
        self.source = source
        self.target = target
        self.style = style

    def __hash__(self):
        return id(self.source) ^ id(self.target)


class Graph(Record):
    __attributes__ = ['nodes', 'edges']

    graph_style = style(
        margin=0,
        nodesep=0,
        ranksep=0,
        splines='splines',
        layout='neato',
        overlap='compress',
    )
    node_style = style(
        shape='box',
        height=0,
        width=0,
        fontname='sans',
        fontsize=10,
        color='none',
        style='filled',
        fillcolor=SILVER
    )
    edge_style = style(
        fontname='sans',
        fontsize=8,
        fontcolor=GRAY,
        arrowsize=0.3,
        color=GRAY
    )

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.ids = {}

    def add_node(self, item, style=None):
        node = Node(item, style)
        self.nodes.add(node)

    def add_edge(self, source, target, style=None):
        edge = Edge(source, target, style)
        self.edges.add(edge)

    def update(self, graph):
        for item, style in graph.nodes:
            self.add_node(item, style)
        for source, target, style in graph.edges:
            self.add_edge(source, target, style)

    def id(self, item):
        item_id = id(item)
        if item_id not in self.ids:
            self.ids[item_id] = len(self.ids)
        return self.ids[item_id]

    @property
    def source(self):
        yield 'digraph G {'
        yield 'graph [{graph_style}];'.format(graph_style=str(self.graph_style))
        yield 'node [{node_style}];'.format(node_style=str(self.node_style))
        yield 'edge [{edge_style}];'.format(edge_style=str(self.edge_style))
        for node in self.nodes:
            pattern = (
                '{index} [{style}];'
                if node.style
                else '{index}'
            )
            yield pattern.format(
                index=self.id(node.item),
                style=str(node.style)
            )
        for edge in self.edges:
            pattern = (
                '{source} -> {target} [{style}];'
                if edge.style
                else '{source} -> {target};'
            )
            yield pattern.format(
                source=self.id(edge.source),
                target=self.id(edge.target),
                style=str(edge.style)
            )
        yield '}'

    def __repr__(self):
        return 'Graph(...)'

    def _repr_pretty_(self, printer, cycle):
        printer.text(repr(self))

    def _repr_svg_(self):
        return dot2svg('\n'.join(self.source))
