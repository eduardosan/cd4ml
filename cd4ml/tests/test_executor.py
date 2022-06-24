import unittest

from concurrent.futures import as_completed

from cd4ml.executor import LocalExecutor
from cd4ml.task import Task


class TestExecutor(unittest.TestCase):
    """Test local executor."""
    def setUp(self) -> None:
        def add(a, b):
            return a + b

        self.task = Task(name='add', task=add)
        self.e = LocalExecutor()

    def tearDown(self) -> None:
        pass

    def test_create_pool(self):
        """Should create a process pool"""
        self.e = LocalExecutor()
        self.assertIsInstance(self.e, LocalExecutor)

    def test_pool_submit(self):
        """Should submit a job to process pool."""
        self.e.submit(self.task, 1, 2)
        self.assertEqual(len(self.e.tasks), 1)

    def test_completed(self):
        """Should return result when a job is completed"""
        self.e.submit(self.task, 1, 2)
        self.e.run()
        self.assertEqual(self.e.output['add'], 3)

    def test_pool_submit_jobs(self):
        """Should submit multiple jobs to process pool"""
        def add(a, b):
            return a + b

        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        self.e.submit(t, 1, 2)
        self.e.submit(t2, 1, 2)
        self.e.submit(t3, 1, 2)
        self.e.submit(t4, 1, 2)
        self.assertEqual(len(self.e.tasks), 4)

    def test_pool_submit_jobs_completed(self):
        """Should submit and run multiple jobs to process pool"""
        def add(a, b):
            return a + b

        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        self.e.submit(t, 1, 2)
        self.e.submit(t2, 1, 2)
        self.e.submit(t3, 1, 2)
        self.e.submit(t4, 1, 2)
        self.e.run()
        print(self.e.output)
        for elm in self.e.output:
            self.assertEqual(self.e.output[elm], 3)
