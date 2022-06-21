from unittest import TestCase
import graphlib

from cd4ml.workflow import Workflow


class TestWorkflow(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_workflow(self):
        """Should start a Workflow"""
        w = Workflow()
        self.assertIsInstance(w, Workflow)
        self.assertIsInstance(w, graphlib.TopologicalSorter)


