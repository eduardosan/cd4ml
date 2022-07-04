from abc import ABC, abstractmethod
from typing import Callable,Union
from cd4ml.contracts.artifact import Artifact

class Model(ABC):
    
    def __init__(self, artifacts:Union[Artifact,list[Artifact]]) -> None:
        '''
        Base class representing the model contract that should be used to put a machine learning model into production
        Any complex object that is used during training or prediction should be stored in the artifacts property.
        .
        '''
        self.artifacts = artifacts
        self._check_artifacts()

    @abstractmethod
    def fit(self,X,y):
        '''
        Method to train the machine learning model. 
        Any complex object that is used during training should be stored as an Artifact class.
        ''' 
        pass
    
    @abstractmethod
    def predict(self,X):
        '''
        Method to make predictions with the machine learning model.
        Any complex object that is used during prediction should be retrieved from the artifacts property.
        '''
        pass    
    
    def _check_artifacts(self):
        if self.artifacts is None or self.artifacts == []:
            raise ValueError("A proper artifacts should be set in order to use the model.")

    @property
    def artifacts(self)-> list[Artifact]:
        '''
        This property contains all object artifacts (Transformers,Estimators, etc) used during fit and that will be used during predict.
        This is to ensure the proper logging into the experiment tracking tool.
        '''
        return self._artifacts

    @artifacts.setter
    def artifacts(self,artifacts:Union[Artifact,list[Artifact]]):
        if isinstance(artifacts,list) and isinstance(artifacts[0],Artifact):
            self._artifacts = artifacts
        elif isinstance(artifacts,Artifact):
            self._artifacts = [artifacts]
        else:
            raise TypeError("artifacts object should be a list of Artifact classes or a single Artifact.")

    @artifacts.getter
    def artifacts_objects(self):
        return [x.object for x in self._artifacts]

    @artifacts.getter
    def artifacts_params(self):
        return [x.params for x in self._artifacts]


class ModelEvaluator:

    def __init__(self,model:Model):
        self.model = model

    def evaluate(self,X,y,metrics:Union[Callable,list[Callable]]):

        y_pred = self.model.predict(X) #Feature Improvement: some metrics might not work with prediction, but with prediction_proba.

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