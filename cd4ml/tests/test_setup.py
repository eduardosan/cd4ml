from unittest import TestCase
import graphlib

from cd4ml.workflow import Workflow


class TestSetup(TestCase):
    def setUp(self) -> None:
        pass

    def test_repository(self):
        """Should start a Workflow"""
        w = Workflow()
        self.assertIsInstance(w, Workflow)
        self.assertIsInstance(w, graphlib.TopologicalSorter)

    def tearDown(self) -> None:
        pass
