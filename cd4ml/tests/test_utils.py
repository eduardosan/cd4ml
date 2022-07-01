import io
import pytest
import unittest

from graphlib import TopologicalSorter

from cd4ml.utils import graph_to_dot


@pytest.mark.usefixtures('get_dotfile')
class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_parse_complex_graph(self):
        """Should parse a complex graph to dotfile."""
        graph = TopologicalSorter()
        graph.add('add')
        graph.add('add2', 'add')
        graph.add('add3', 'add')
        graph.add('add6', 'add')
        graph.add('add9')
        graph.add('add4', 'add2')
        graph.add('add5', 'add2')
        graph.add('add7', 'add5')
        graph.add('add8', 'add6')

        dot = graph_to_dot(graph)

        dotfile = io.open(self.dotfile).read()
        self.assertListEqual(dot.split(), dotfile.split())
