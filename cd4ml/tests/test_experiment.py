import os.path
import unittest
import pytest

import pandas as pd

from cd4ml.experiment import LocalExperimentProvider, Experiment


@pytest.mark.usefixtures('get_local_experiment_repository')
class LocalExperimentProviderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = LocalExperimentProvider(repository_path=self.local_experiment_repository)
        self.filepath = os.path.join(self.provider.repository_path, './teste.json')

    def tearDown(self) -> None:
        try:
            # Remove test file for every run
            os.unlink(self.filepath)
        except FileNotFoundError:
            pass

    def test_experiment_init(self):
        """Should create a directory for experiment data."""
        self.assertTrue(os.path.exists(self.provider.repository_path))

    def test_experiment_data_save(self):
        """Should save data on experiment repository."""
        teste = {'a': 'abcde'}
        self.provider.save(path='teste.json', data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_save_pandas(self):
        """Should save a pandas DataFrame to experiment repository"""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider._save_pandas(path=self.filepath, data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_data_load(self):
        """Should load data from experiment repository."""
        teste = {'a': 'abcde'}
        self.provider.save(path='teste.json', data=teste)
        test_data = self.provider.load(self.filepath)
        self.assertDictEqual(teste, test_data)

    def test_experiment_load_pandas(self):
        """Should load data from experiment repository and return it as a pandas DataFrame."""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider._save_pandas(path=self.filepath, data=teste)
        test_data = self.provider._load_pandas(self.filepath)
        self.assertTrue(teste.equals(test_data))

    def test_experiment_save_with_pandas(self):
        """Standard save method should accept a pandas DataFrame"""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider.save(path='teste.json', data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_load_with_pandas(self):
        """Should use standard load data with a flag to return data as pandas."""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider._save_pandas(path=self.filepath, data=teste)
        test_data = self.provider.load('teste.json', pandas=True)
        self.assertTrue(teste.equals(test_data))


@pytest.mark.usefixtures('get_local_experiment_repository')
class ExperimentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = LocalExperimentProvider(repository_path=self.local_experiment_repository)

    def tearDown(self) -> None:
        pass

    def test_executor_experiments_class(self):
        """Should instantiate the experiments class."""
        e = Experiment(provider=self.provider)
        self.assertIsInstance(e, Experiment)
        self.assertIsInstance(e.provider, LocalExperimentProvider)

    def test_executor_experiments_repository(self):
        """Should create a repository for experiments data."""
        e = Experiment(provider=self.provider)
        self.assertTrue(os.path.exists(e.provider.repository_path))

    def test_executor_experiments_output(self):
        """Should create experiments output data repository"""
        e = Experiment(provider=self.provider)
        new_path = e.provider.add_path(path='out', name='output')
        self.assertTrue(os.path.exists(new_path))

    def test_executor_experiments_output_data(self):
        """Should store experiments output data in repository"""
        pass
