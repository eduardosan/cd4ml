
from joblib import dump, load

from cd4ml.contracts.artifact import Artifact, ArtifactsHandler

class DiabetesArtifactHandler(ArtifactsHandler):
    
    def __init__(self,path) -> None:
        self.path = path

    def save(self,artifacts:list[Artifact]):
        estimator, scaler = artifacts
        dump(estimator.object, self.path+f'/{estimator.name}.joblib') 
        dump(scaler.object, self.path+f'/{scaler.name}.joblib')

    def load(self,parameters:dict) -> list[Artifact]:
        artifacts = []
        
        model_params = parameters['model_params']
        estimator = load(self.path+'/model.joblib') 
        artifacts.append(Artifact(name='model',object=estimator,params=model_params))
        
        scaler_params = parameters['scaler_params']
        scaler = load(self.path+'/scaler.joblib') 
        artifacts.append(Artifact(name='scaler',object=scaler,params=scaler_params))

        return artifacts