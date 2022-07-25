import os
import json

from abc import ABC, abstractmethod
import pandas as pd

from cd4ml.log import logger


class Experiment:
    def __init__(self, provider, experiment_id='latest'):
        assert isinstance(provider, ExperimentProvider)
        self.provider = provider
        self.experiment_id = experiment_id
        self.provider.add_path(path=experiment_id, name='root')
        self.output_path = 'output'
        self.params_path = 'params'

        # Load experiment metadata
        self._init_experiment()

    def _init_experiment(self):
        # Try to load experiment metadata from provider
        try:
            metadata = self.provider.load(name='.metadata')

            # Load output paths to provider
            self.provider.paths = metadata['output']
        except DataNotFound:
            logger.info(f"Creating metadata for experiment = '{self.experiment_id}' at {self.provider.repository_path}")
            metadata = {
                'experiment_id': self.experiment_id,
                'output': {},
                'params': {}
            }
            self.provider.save(name='.metadata', data=metadata)

        self.metadata = metadata

    def save_output(self, name, data):
        """
        Should save experiment output to provider

        :param str name: Output experiment name
        :param dict, pd.DataFrame data: Data to be saved on provider
        :return str: Path on provider where the experiment was saved
        """
        self.provider.add_path(path=self.output_path, name='output')
        output = self.provider.save(name=name, data=data, path=self.output_path)

        # Add output data to metadata
        self.metadata['output'][name] = output
        self.provider.save(name='.metadata', data=self.metadata, path='root')
        return output

    def load_output(self, name, pandas=False):
        """
        Load previously stored output on provider

        :param str name: Name of data file to be loaded from output
        :param bool pandas: Should we return it as pandas DataFrame
        :return dict, pd.DataFrame: output data on desired format
        """
        output = self.provider.load(name=name, pandas=pandas, path=self.output_path)
        return output

    def save_params(self, name, data: dict):
        """
        Save params on experiment provider

        :param str name: A name to be added to params. Should be the same task name
        :param dict data: params in kwargs format
        :return str: Path on provider where the params were saved
        """
        self.provider.add_path(path=self.params_path, name='params')
        output = self.provider.save(name=name, data=data, path=self.params_path)

        # Add params to metadata
        self.metadata['params'][name] = output
        self.provider.save(name='.metadata', data=self.metadata, path='root')
        return output

    def load_params(self, name):
        """
        Load previously stored output on provider

        :param str name: Name of task to retrieve params from output
        :return dict: params in kwargs format
        """
        output = self.provider.load(name=name, pandas=False, path=self.params_path)
        return output


class ExperimentProvider(ABC):

    def __init__(self, repository_path):
        self.repository_path = repository_path
        self.paths = dict()
        super().__init__()

    @abstractmethod
    def save(self, name, data, datatype='json', path='root'):
        """
        Save data on repository.

        :param str name: Path in the experiment repository. Defaults to root
        :param str path: Path to save data with filename, relative to experiment repository.
        :param dict, pd.DataFrame data: Data dictionary
        :param str datatype: Data type to save on experiments repository. Can be one of the following:

            * ``'json'``: standard JSON type to save dicts
            * ``'csv'``: CSV file to serialize
        :return: Data loaded from repository
        :rtype: str
        :example:

        >>>  teste = {'col1': [1, 2], 'col2': [3, 4]}
        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> p.save(path='teste', data=teste)
        '.cd4ml/teste.json'
        >>> p.paths
        {
            'teste': '.cd4ml/teste.json'
        }

        >>>  teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> p.save(path='teste.json', data=teste)
        '.cd4ml/teste.json'
        >>> p.paths
        {
            'teste': '.cd4ml/teste.json'
        }

        """
        pass

    @abstractmethod
    def load(self, name, pandas=False, path='root', datatype='json'):
        """
        Load data from repository.

        :param str name: Name of the data to be recovered on experiment
        :param str path: Path where data is stored without filename, relative to experiment repository.
        :param bool pandas: Should we return a pandas dataframe
        :param str datatype: Data type to save on experiments repository. Can be one of the following:

            * ``'json'``: standard JSON type to save dicts
            * ``'csv'``: CSV file to serialize
        :return: The loaded data
        :rtype: dict, pd.DataFrame
        :example:

        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> output = p.load('teste', pandas=True)
        >>> print(output)

        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> output = p.load('teste', pandas=False)
        >>> print(output)
        {
            'col1': [1, 2],
            'col2': [3, 4]
        }
        >>> print(p.paths)
        {
            'teste': '.cd4ml/teste.json'
        }
        """
        pass

    @abstractmethod
    def add_path(self, path, name):
        """
        Add a new path to experiments repository. It could be a new folder or anything else supported by the
        repository. Let's suppose the repository_path is set to ``'.cd4ml'``. This method will add a new folder to path
        and a new registered path to the list of available paths.

        :param path: Path to be added in repository
        :type path: str
        :param name: Name of the path to be added in repository
        :type name: str
        :return: Absolute path added to repository
        :rtype: str
        :example:

        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> output = p.add_path(path='out', name='output')
        >>> print(output)
        '.cd4ml/out'
        """
        pass


class LocalExperimentProvider(ExperimentProvider):

    def __init__(self, repository_path='.cd4ml'):
        super(LocalExperimentProvider, self).__init__(repository_path)
        # make sure local directory exists
        os.makedirs(self.repository_path, exist_ok=True)

    def save(self, name, data, datatype='json', path='root'):
        root_path = self.repository_path
        if path != 'root':
            root_path = os.path.join(self.repository_path, path)
        filepath = os.path.join(root_path, f'{name}.{datatype}')
        with open(filepath, 'w+') as fd:
            if isinstance(data, pd.DataFrame):
                filepath = self._save_pandas(path=filepath, data=data)
            else:
                json.dump(data, fd)

        return filepath

    def load(self, name, pandas=False, path='root', datatype='json'):
        root_path = self.repository_path
        if path != 'root':
            root_path = os.path.join(self.repository_path, path)
        filepath = os.path.join(root_path, f'{name}.{datatype}')
        if pandas:
            return self._load_pandas(filepath)
        try:
            with open(filepath, 'r') as fd:
                return json.load(fd)
        except FileNotFoundError as e:
            raise DataNotFound(e)

    def _save_pandas(self, path, data: pd.DataFrame, orient='records', lines=True, *args, **kwargs):
        """
        Save pandas to data repository
        :param path: Path where data is stored with filename, relative to experiment repository
        :type path: str
        :param data: Instance of a pandas DataFrame
        :type data: pd.DataFrame
        :param orient: pandas to_json orient definition like `official documentation
            <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html>`, defaults to 'records'
        :type orient: str
        :param lines: pandas to_json lines attribute definition like `official documentation
            <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html>`, defaults to True
        :type lines: bool
        :param args:
        :param kwargs:
        :return:
        """
        data.to_json(path, orient=orient, lines=lines, *args, **kwargs)
        return path

    def _load_pandas(self, path, orient='records', lines=True, *args, **kwargs):
        """
        Load a pandas dataframe
        :param path: Path where data is stored with filename, relative to experiment repository
        :type path: str
        :param orient: pandas read_json orient definition like `official documentation
            <https://pandas.pydata.org/docs/reference/api/pandas.read_json.html>`, defaults to 'records'
        :type orient: str
        :param lines: pandas read_json lines attribute definition like `official documentation
            <https://pandas.pydata.org/docs/reference/api/pandas.read_json.html>`, defaults to True
        :type lines: bool
        :param args:
        :param kwargs:
        :return: Return a DataFrame
        :rtype: pd.DataFrame
        """
        return pd.read_json(path, orient=orient, lines=lines, *args, **kwargs)

    def add_path(self, path, name):
        new_path = os.path.join(self.repository_path, path)
        os.makedirs(new_path, exist_ok=True)
        return new_path


class DataNotFound(Exception):
    """Should be raised when data is not found on provider"""
    pass
