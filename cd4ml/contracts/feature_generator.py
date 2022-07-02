from abc import ABC, abstractmethod
import pandas as pd


# TODO: Fazer retorno direto, sem propriedades.?????

class FeatureGenerator(ABC):

    @abstractmethod
    def generate_features(self, data:pd.DataFrame)-> pd.DataFrame:
        '''Method to generate feature data. Data should be stored in this class using the data property.'''
        pass

    @abstractmethod
    def generate_target(self, data:pd.DataFrame):
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