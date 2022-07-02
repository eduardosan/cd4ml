from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    '''
    Abstract class representing data processing steps that go into production.
    '''
    @abstractmethod
    def load_data(self) -> Any:
        '''Method to load the data into memory from a given path. Data should be stored in this class using the data property.'''
        pass

    @abstractmethod
    def preprocess(self,raw_data:Any)-> Any:
        '''Method to preprocess the data. Data should be stored in this class using the data property.'''
        pass

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self,raw_data):
        self._raw_data = raw_data

    @property
    def processed_data(self):
        return self._processed_data

    @processed_data.setter
    def processed_data(self,processed_data):
        self._processed_data = processed_data