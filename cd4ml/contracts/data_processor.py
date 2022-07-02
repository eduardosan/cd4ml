from abc import ABC, abstractmethod
import pandas as pd

class DataProcessor(ABC):

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        '''Method to load the data into memory from a given path. Data should be stored in this class using the data property.'''
        pass

    @abstractmethod
    def preprocess(self,data:pd.DataFrame) -> pd.DataFrame:
        '''Method to preprocess the data. Data should be stored in this class using the data property.'''
        pass

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self,raw_data):
        self._raw_data = raw_data

    @raw_data.deleter
    def raw_data(self):
        del self._raw_data

    @property
    def processed_data(self):
        return self._processed_data

    @processed_data.setter
    def processed_data(self,processed_data):
        self._processed_data = processed_data

    @raw_data.deleter
    def raw_data(self):
        del self._raw_data