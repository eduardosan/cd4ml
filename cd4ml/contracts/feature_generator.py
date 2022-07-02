from abc import ABC, abstractmethod
import pandas as pd


class FeatureGenerator(ABC):
    '''
    Abstract class representing feature generation process that goes into production.
    '''
    @abstractmethod
    def get_features(self, data:pd.DataFrame)-> pd.DataFrame:
        '''Method to generate feature data. Data should be stored in this class using the data property.'''
        pass

    @abstractmethod
    def get_target(self, data:pd.DataFrame):
        pass

    @property
    def features(self):
        return self._features
    
    @features.setter
    def features(self,features):
        self._features = features
        
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self,target):
        self._target = target