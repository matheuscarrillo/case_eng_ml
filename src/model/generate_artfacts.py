# import os
# path = r"C:\Users\mathe\OneDrive\Área de Trabalho\POS_TECH\case_engml\case_software_engineer"
# os.chdir(path)
# print("Diretório atual:", os.getcwd())

import pickle
from utils.transformer import JsonToDF, FeatureEngineering, Model
from sklearn.pipeline import Pipeline

model = pickle.load(open('modelo/model.pkl', 'rb'))


# Transform JSON to DataFrame
json_to_df = JsonToDF()

# Feature Engineering
feature_engineering = FeatureEngineering(
        features = model.feature_names_in_,
        ignored_cols=["PassengerId", "Name", "Ticket", "Cabin", "Survived"]
        )

# Model Prediction
predict = Model(model=model)

pipe = Pipeline([
        ('json_to_df', json_to_df), 
        ('feature_engineering',feature_engineering),
        ('model', predict)])

with open('src/model/pipeline_model.pkl', 'wb') as f:
    pickle.dump(pipe, f)