import pickle
import json
import pandas as pd


class JsonToDF:
    def __init__(self):
        pass

    def transform(self, json_data):
        X = pd.DataFrame(json_data)
        return X

class FeatureEngineering:
    def __init__(self, features,  ignored_cols):
        self.features = features
        self.ignored_cols = ignored_cols

    def transform(self, X):
        X['Embarked_S'] = X['Embarked'].eq('S').astype(int)
        X['Embarked_Q'] = X['Embarked'].eq('Q').astype(int)
        X['Sex_male'] = X['Sex'].eq('male').astype(int)
        X = X[self.features]    
        return X

class Model:
    def __init__(self, model):
        self.model = model

    def fit(self):
        pass
        
    def predict(self, X):
        y_pred_test = self.model.predict_proba(X)
        
        return {
            'output':float(y_pred_test[-1][0])
        }
