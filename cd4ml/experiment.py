import os
import json

from abc import ABC, abstractmethod
import pandas as pd


class Experiment:
    def __init__(self, provider, experiment_id='latest'):
        assert isinstance(provider, ExperimentProvider)
        self.provider = provider
        self.experiment_id = experiment_id
        self.provider.add_path(experiment_id, 'root')
        self.output_path = 'output'

    def save_output(self, name, data):
        """
        Should save experiment output to provider

        :param str name: Output experiment name
        :param dict, pd.DataFrame data: Data to be saved on provider
        :return str: PAth on provider where the experiment was saved
        """
        self.provider.add_path(path=self.output_path, name=self.output_path)
        output = self.provider.save(path=f'{self.output_path}/{name}', data=data)
        return output

    def load_output(self, name, pandas=False):
        """
        Load previously stored output on provider

        :param str name: Name of data file to be loaded from output
        :param bool pandas: Should we return it as pandas DataFrame
        :return dict, pd.DataFrame: output data on desired format
        """
        output = self.provider.load(path=f'{self.output_path}/{name}', pandas=pandas)
        return output


class ExperimentProvider(ABC):

    def __init__(self, repository_path):
        self.repository_path = repository_path
        self.paths = dict()
        super().__init__()

    @abstractmethod
    def save(self, path, data):
        """
        Save data on repository.

        :param str path: Path to save data with filename, relative to experiment repository.
        :param dict, pd.DataFrame data: Data dictionary
        :return: Data loaded from repository
        :rtype: str
        :example:

        >>>  teste = {'col1': [1, 2], 'col2': [3, 4]}
        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> p.save(path='teste.json', data=teste)
        '.cd4ml/teste.json'

        >>>  teste = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> p.save(path='teste.json', data=teste)
        '.cd4ml/teste.json'

        """
        pass

    @abstractmethod
    def load(self, path, pandas=False):
        """
        Load data from repository.

        :param str path: Path where data is stored with filename, relative to experiment repository.
        :param bool pandas: Should we return a pandas dataframe
        :return: The loaded data
        :rtype: dict, pd.DataFrame
        :example:

        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> output = p.load('teste.json', pandas=True)
        >>> print(output)

        >>> p = LocalExperimentProvider(repository_path='.cd4ml')
        >>> output = p.load('teste.json', pandas=False)
        >>> print(output)
        {
            'col1': [1, 2],
            'col2': [3, 4]
        }
        """
        pass

    @abstractmethod
    def add_path(self, path, name):
        """Add a new path to experiments repository. It could be a new folder or anything else supported by the
        repository. Let's suppose the repository_path is set to ``'.cd4ml'``. This method will add a new folder to path and
        a new registered path to the list of available paths::

            p = LocalExperimentProvider(repository_path='.cd4ml')
            output = p.add_path(path='out', name=output)
            print(output)
            '.cd4ml/out'
            print(p.paths)

            {
                'output': '.cd4ml/out'
            }

        :param path: Path to be added in repository
        :type path: str
        :param name: Name of the path to be added in repository
        :type name: str
        :return: Absolute path added to repository
        :rtype: str
        """
        pass


class LocalExperimentProvider(ExperimentProvider):

    def __init__(self, repository_path='.cd4ml'):
        super(LocalExperimentProvider, self).__init__(repository_path)
        # make sure local directory exists
        os.makedirs(self.repository_path, exist_ok=True)

    def save(self, path, data):
        filepath = os.path.join(self.repository_path, path)
        with open(filepath, 'w+') as fd:
            if isinstance(data, pd.DataFrame):
                filepath = self._save_pandas(path=filepath, data=data)
            else:
                json.dump(data, fd)

        return filepath

    def load(self, path, pandas=False):
        filepath = os.path.join(self.repository_path, path)
        if pandas:
            return self._load_pandas(filepath)
        with open(filepath, 'r') as fd:
            return json.load(fd)

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
        self.paths = {name: new_path}
        return new_path

