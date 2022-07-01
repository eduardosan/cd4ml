import copy

from graphlib import TopologicalSorter


def get_graph(graph: TopologicalSorter):
    import pygraphviz as pgv
    g = pgv.AGraph(directed=True)
    g.add_node("start", shape="doublecircle")

    # Copy all objects to avoid closing the graph
    tmpgraph = copy.copy(graph)

    # Add all elements to the graph
    tmpgraph.prepare()

    # Start with first element
    for elm in tmpgraph.get_ready():
        g = parse_node(ts=tmpgraph, parent='start', node=elm, agraph=g)

    return g


def graph_to_dot(graph: TopologicalSorter):
    """
    Parse a graph in Topological sorter
    :param graph:
    :return:
    """
    g = get_graph(graph)

    # Generate dotfile in tmp dir
    return g.to_string()


def parse_node(ts: TopologicalSorter, parent, node, agraph):
    """
    Generate a graph from the node

    :param node:
    :return:
    """
    import pygraphviz as pgv

    # Type checking here to avoid breaking without graphviz
    assert isinstance(agraph, pgv.AGraph)

    agraph.add_edge(parent, node)
    for elm in ts._get_nodeinfo(node).successors:
        # Add new edge for every sucessor
        parse_node(ts, node, elm, agraph)

    return agraph


def draw_graph(graph: TopologicalSorter, filepath=None):
    """
    Draw SVG representation for the graph
    :param graph: pgv.Agraph   A graph object
    :param filepath: str    filepath to image file output
    :return: object with draw
    """
    g = get_graph(graph)
    g.layout(prog='dot')

    if filepath is not None:
        g.draw(filepath)
    return g
