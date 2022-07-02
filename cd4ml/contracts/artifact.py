from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable,Union

@dataclass
class Artifact:
    name:str
    object:Any
    params:dict
    path:str = ''

class ArtifactsHandler(ABC):
    
    @abstractmethod
    def save(artifacts:list[Artifact],path:str):
        pass
    
    @abstractmethod
    def load(parameters:dict,path:str)->list[Artifact]:
        pass