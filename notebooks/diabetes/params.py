from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.model_selection import train_test_split

def rmse(y_true,y_pred):
    return mean_squared_error(y_true,y_pred,squared=False)

data_processor_params = {
    'loader':load_diabetes
}

feature_generator_params = {
}

model_params = {
    'model':Ridge,
    'model_params':{'fit_intercept':True,'solver':'lsqr','alpha':0.5},
    'scaler':MinMaxScaler,
    'scaler_params':{'feature_range':[0,1]}
}

evaluator_params = {
    'metrics':[rmse,mean_squared_error,mean_absolute_error]
}

artifacts_handler_parameters = {
    'model_params':model_params['model_params'],
    'scaler_params':model_params['scaler_params']
}