import unittest
from collections import OrderedDict

from cd4ml.task import Task


def add(a, b):
    return a + b


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
        t = Task(name='sum', task=add)
        self.assertIsInstance(t, Task)
        self.assertTrue(callable(t.task))

    def test_task_function_exec(self):
        """Should execute a python function as a task and return results."""
        t = Task(name='sum', task=add)
        result = t.run(1, 2)
        self.assertEqual(result, 3)

    def test_task_function_params(self):
        """Should store function params in task"""
        t = Task(name='sum', task=add)
        self.assertEqual(t.params['a'].name, 'a')
        self.assertEqual(t.params['b'].name, 'b')

    def test_task_function_no_params(self):
        """Should return empty list if there is no params in function."""
        def hello():
            print("Oi")

        t = Task(name='hello', task=hello)
        self.assertEqual(t.params, OrderedDict())

    def test_task_simple_param(self):
        """Should execute a task with a single text param."""
        def get_url(url):
            return url

        t = Task(name='url', task=get_url)
        result = t.run('http://test.com')
        self.assertEqual(result, 'http://test.com')

    def test_task_simple_named_param(self):
        """Should execute a task with a single text param."""
        def get_url(url):
            return url

        t = Task(name='url', task=get_url)
        result = t.run(url='http://test.com')
        self.assertEqual(result, 'http://test.com')

