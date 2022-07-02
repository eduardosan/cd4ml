from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable,Union
import pandas as pd

@dataclass
class Artifact:
    name:str
    output_path:str
    object:Any

class Model(ABC):

    @abstractmethod
    def fit(self,X,y):
        '''Method to train the machine learning model.'''
        pass
    
    @abstractmethod
    def predict(self,X):
        '''Method to make predictions with the machine learning model.'''
        pass
    
    @abstractmethod
    def load(self,path):
        '''Method to load the machine learning model into memory.'''
        pass
    
    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self,params:list[Artifact]):
        self._parameters = params
    
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self,model):
        self._model = model

class ModelEvaluator:

    def __init__(self,model):
        self.model = model

    def evaluate(self,X,y,metrics:Union[Callable,list[Callable]]):

        y_pred = self.model.predict(X) #Improvement: some metrics might not work with prediction, but with prediction_proba.

        metric_values = {}

        for metric in metrics:
            metric_name = metric.__name__
            metric_values[metric_name] = metric(y_pred,y) 
        self.metrics = metric_values
        
        return self.metrics
        
    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self,metrics:dict):
        self._metrics = metrics