import pandas as pd

from cd4ml.contracts.data_processor import DataProcessor

class DiabetesDataProcessor(DataProcessor):
    
    def __init__(self,loader) -> None:
        self._loader = loader
    
    def load_data(self) -> pd.DataFrame:
        diabetes = self._loader(as_frame=True)
        df = diabetes.data
        df['target'] = diabetes.target
        self.raw_data = df
        return df

    def preprocess(self,raw_data:pd.DataFrame) -> pd.DataFrame:
        df = self._encode_sex_feature(raw_data)
        self.processed_data = df
        return df

    def _encode_sex_feature(self,df:pd.DataFrame):
        df_encoded = df.copy()
        df_encoded.loc[(df['sex'] == -0.044642),['sex']] = 1
        df_encoded.loc[df['sex'] != -0.044642,['sex']] = 0
        return df_encoded
