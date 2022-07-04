import pandas as pd

from cd4ml.contracts.artifact import Artifact
from cd4ml.contracts.model import Model

class DiabetesModel(Model):
    
    def __init__(self, model, model_params, scaler, scaler_params) -> None:
        self.model = model(**model_params)
        self.scaler = scaler(**scaler_params)
        super().__init__(artifacts = [
                                Artifact(name='model',object = self.model,params = model_params),
                                Artifact(name='scaler',object = self.scaler,params = scaler_params)])

    def fit(self, X:pd.DataFrame, y:pd.DataFrame):
        estimator,scaler = self.artifacts_objects
        scaler.fit(X)
        X_norm = scaler.transform(X)
        estimator.fit(X_norm,y)
    
    def predict(self, X):
        estimator,scaler = self.artifacts_objects
        X_norm = scaler.transform(X)
        return estimator.predict(X_norm)

