from unittest import TestCase
import graphlib

from cd4ml.workflow import Workflow
from cd4ml.task import Task


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

    def test_add_task(self):
        """Should add a new task to the Workflow."""
        def add(a, b):
            return a + b

        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        self.assertIsInstance(w.tasks['add'], Task)

    def test_add_task_run(self):
        """Should add a task run with params for execution."""
        def add(a, b):
            return a + b

        w = Workflow()
        t = Task(name='add', task=add)
        w.add_task(t)
        result = w.run_task('add', 1, 2)
        self.assertEqual(result, 3)
