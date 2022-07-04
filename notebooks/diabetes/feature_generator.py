import pandas as pd

from cd4ml.contracts.feature_generator import FeatureGenerator

class DiabetesFeatureGenerator(FeatureGenerator):
    
    def get_features(self, data: pd.DataFrame) -> pd.DataFrame:
        if 'target' in data.columns:
            return data.drop(columns=['target'])
        else:
            return data
        
    def get_target(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            return data['target']
        except Exception as e:
            print(e)
