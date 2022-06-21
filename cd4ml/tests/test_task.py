import unittest

from cd4ml.task import Task


class TestTask(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_task(self):
        """Should instantiate a general Task."""
        t = Task(name='task1')
        self.assertIsInstance(t, Task)
        self.assertEqual(t.name, 'task1')
        self.assertEqual(t.description, 'task1')

    def test_task_function(self):
        """Should instantiate a general python function as a task."""
        def add(a, b):
            return a + b

        t = Task(name='sum', task=add)
        self.assertIsInstance(t, Task)
        self.assertTrue(callable(t.task))

    def test_task_function_exec(self):
        """Should execute a python function as a task and return results."""
        def add(a, b):
            return a + b

        t = Task(name='sum', task=add)
        result = t.run(1, 2)
        self.assertEqual(result, 3)
