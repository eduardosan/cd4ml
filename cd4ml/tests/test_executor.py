import os.path

import unittest
import pytest

from cd4ml.executor import LocalExecutor
from cd4ml.task import Task
from cd4ml.experiment import LocalExperimentProvider, Experiment


def add(a, b):
    return a + b


@pytest.mark.usefixtures('get_local_experiment_repository')
class TestLocalExecutor(unittest.TestCase):
    """Test local executor."""
    def setUp(self) -> None:
        def add(a, b):
            return a + b

        self.task = Task(name='add', task=add)
        provider = LocalExperimentProvider(repository_path=self.local_experiment_repository)
        exp = Experiment(provider=provider)
        self.e = LocalExecutor(experiment=exp)

    def tearDown(self) -> None:
        pass

    def test_create_pool(self):
        """Should create a process pool"""
        self.e = LocalExecutor()
        self.assertIsInstance(self.e, LocalExecutor)

    def test_pool_submit(self):
        """Should submit a job to process pool."""
        self.e.submit(self.task, params={'a': 1, 'b': 2})
        self.assertEqual(len(self.e.tasks), 1)

    def test_pool_submit_format(self):
        """Should fail if format submitted is other than dict."""
        with self.assertRaises(TypeError):
            self.e.submit(self.task, (1, 2))

    def test_completed(self):
        """Should return result when a job is completed"""
        self.e.submit(self.task, params={'a': 1, 'b': 2}, output='add')
        self.e.run()
        self.assertEqual(self.e.output['add'], 3)

    def test_pool_submit_jobs(self):
        """Should submit multiple jobs to process pool"""
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        self.e.submit(t, params={'a': 1, 'b': 2})
        self.e.submit(t2, params={'a': 1, 'b': 2})
        self.e.submit(t3, params={'a': 1, 'b': 2})
        self.e.submit(t4, params={'a': 1, 'b': 2})
        self.assertEqual(len(self.e.tasks), 4)

    def test_pool_submit_jobs_completed(self):
        """Should submit and run multiple jobs to process pool"""
        t = Task(name='add', task=add)
        t2 = Task(name='add2', task=add)
        t3 = Task(name='add3', task=add)
        t4 = Task(name='add4', task=add)
        self.e.submit(t, params={'a': 1, 'b': 2}, output='add')
        self.e.submit(t2, params={'a': 1, 'b': 2}, output='add2')
        self.e.submit(t3, params={'a': 1, 'b': 2}, output='add3')
        self.e.submit(t4, params={'a': 1, 'b': 2}, output='add4')
        self.e.run()
        print(self.e.output)
        for elm in self.e.output:
            self.assertEqual(self.e.output[elm], 3)

    def test_executor_experiments_repository(self):
        """Should create a repository for experiments data."""
        self.assertTrue(os.path.exists(self.e.experiment.provider.repository_path))

    def test_executor_experiments_output(self):
        """Should store experiments output on data repository"""
        self.e.submit(self.task, params={'a': 1, 'b': 2}, output='add')
        self.e.run()
        output = self.e.experiment.load_output(name='add')
        self.assertEqual(output, 3)
