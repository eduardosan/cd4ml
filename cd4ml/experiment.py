import os
import json

from abc import ABC, abstractmethod
import pandas as pd


class Experiment:
    def __init__(self, provider, experiment_id='latest'):
        assert isinstance(provider, ExperimentProvider)
        self.provider = provider


class ExperimentProvider(ABC):

    def __init__(self, repository_path):
        self.repository_path = repository_path
        self.paths = dict()
        super().__init__()

    @abstractmethod
    def save(self, path, data):
        """
        Save data on repository
        :param path: Path to save data with filename, relative to experiment repository
            Ex.: repository = '.cd4ml'
                data = 'output/teste.json
                filepath = '.cd4ml/output/teste.json
        :type path: str
        :param data: Data dictionary
        :type data: dict or pd.DataFrame
        :return: Data loaded from repository
        :rtype: dict
        """
        pass

    @abstractmethod
    def load(self, path, pandas=False):
        """
        Load data from repository
        :param path: Path where data is stored with filename, relative to experiment repository
            Ex.: repository = '.cd4ml'
                data = 'output/teste.json
                filepath = '.cd4ml/output/teste.json
        :type path: str
        :param pandas: Should we return a pandas dataframe
        :type pandas: bool
        :return: The loaded data
        :rtype: dict or pd.DataFrame
        """
        pass

    @abstractmethod
    def add_path(self, path, name):
        """
        Add a new path to experiments repository. It could be a new folder or anything else supported by the repository.
        Let's the repository_path is set to '.cd4ml'. This method will add a new folder to path and a new registered
        path to the list of available paths

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
        if pandas:
            return self._load_pandas(path)
        filepath = os.path.join(self.repository_path, path)
        with open(filepath, 'r') as fd:
            return json.load(fd)

    def _save_pandas(self, path, data: pd.DataFrame, *args, **kwargs):
        """
        Save pandas to data repository
        :param path: Path where data is stored with filename, relative to experiment repository
        :type path: str
        :param data: Instance of a pandas DataFrame
        :type data: pd.DataFrame
        :param args:
        :param kwargs:
        :return:
        """
        data.to_json(path, *args, **kwargs)
        return path

    def _load_pandas(self, path, *args, **kwargs):
        """
        Load a pandas dataframe
        :param path: Path where data is stored with filename, relative to experiment repository
        :type path: str
        :param args:
        :param kwargs:
        :return: Return a DataFrame
        :rtype: pd.DataFrame
        """
        return pd.read_json(path, *args, **kwargs)

    def add_path(self, path, name):
        new_path = os.path.join(self.repository_path, path)
        os.makedirs(new_path, exist_ok=True)
        self.paths = {name: new_path}
        return new_path

