import os.path
import unittest
import pytest
import shutil

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
        self.provider.save(name='teste', data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_save_pandas(self):
        """Should save a pandas DataFrame to experiment repository"""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider._save_pandas(path=self.filepath, data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_data_load(self):
        """Should load data from experiment repository."""
        teste = {'a': 'abcde'}
        self.provider.save(name='teste', data=teste)
        test_data = self.provider.load(name='teste')
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
        self.provider.save(name='teste', data=teste)
        self.assertTrue(os.path.exists(self.filepath))

    def test_experiment_load_with_pandas(self):
        """Should use standard load data with a flag to return data as pandas."""
        teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.provider._save_pandas(path=self.filepath, data=teste)
        test_data = self.provider.load(name='teste', pandas=True)
        self.assertTrue(teste.equals(test_data))


@pytest.mark.usefixtures('get_local_experiment_repository')
class ExperimentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = LocalExperimentProvider(repository_path=self.local_experiment_repository)
        self.e = Experiment(provider=self.provider)

    def tearDown(self) -> None:
        # Remove directory for experiments on every run
        shutil.rmtree(self.local_experiment_repository)

    def test_executor_experiments_class(self):
        """Should instantiate the experiments class."""
        self.assertIsInstance(self.e, Experiment)
        self.assertIsInstance(self.e.provider, LocalExperimentProvider)

    def test_executor_experiments_repository(self):
        """Should create a repository for experiments data."""
        self.assertTrue(os.path.exists(self.e.provider.repository_path))

    def test_executor_experiments_output(self):
        """Should create experiments output data repository"""
        new_path = self.e.provider.add_path(path='out', name='out')
        self.assertTrue(os.path.exists(new_path))

    def test_executor_experiments_output_data(self):
        """Should store experiments output data in repository"""
        output = self.e.save_output(name='teste', data={'col1': [1, 2], 'col2': [3, 4]})
        self.assertTrue(os.path.exists(output))

    def test_executor_experiments_load_output(self):
        """Should load experiments output stored on provider"""
        data = {'col1': [1, 2], 'col2': [3, 4]}
        self.e.save_output(name='test', data=data)
        output = self.e.load_output(name='test')
        self.assertDictEqual(output, data)

    def test_executor_experiments_load_output_pandas(self):
        """Should load experiments output stored on provider as pandas dataframe"""
        data = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        self.e.save_output(name='test', data=data)
        output = self.e.load_output(name='test', pandas=True)
        self.assertTrue(data.equals(output))

    def test_executor_experiments_params(self):
        """Should read experiments params from data repository"""
        self.e.save_params(name='add', data={'a': 1, 'b': 2})
        params = self.e.load_params(name='add')
        self.assertDictEqual({'a': 1, 'b': 2}, params)

    def test_experiment_create_metadata(self):
        """Should create experiment run configuration metadata"""
        self.e.save_params(name='add', data={'a': 1, 'b': 2})
        data = {'col1': [1, 2], 'col2': [3, 4]}
        self.e.save_output(name='test', data=data)
        metadata = {
            'experiment_id': 'latest',
            'output': {
                'test': os.path.join(self.e.provider.repository_path, 'output/test.json')
            },
            'params': {
                'add': os.path.join(self.e.provider.repository_path, 'params/add.json')
            }
        }
        self.assertDictEqual(metadata, self.e.metadata)

    def test_experiment_load_metadata(self):
        """Should load previously saved experiment metadata."""
        self.e.save_params(name='add', data={'a': 1, 'b': 2})
        data = {'col1': [1, 2], 'col2': [3, 4]}
        self.e.save_output(name='test', data=data)

        # This new experiment should load metadata from previously saved repository
        e2 = Experiment(provider=self.provider)
        self.assertDictEqual(e2.metadata, self.e.metadata)
