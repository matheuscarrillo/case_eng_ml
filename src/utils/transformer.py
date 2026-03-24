import pickle
import json
import pandas as pd


def criar_sobrevivente(event, table, pipe):
    body = json.loads(event.get("body", "{}"))
    data = body.get("data")

    results = []

    for item in data:
        pred = pipe.predict([item])

        result = {
            "PassengerId": item["PassengerId"],
            "probabilidade_sobrevivencia": str(round(float(pred["output"]), 2))
        }

        table.put_item(
            Item=result
        )
        
        results.append(result)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }

def listar_sobreviventes(table):
    response = table.scan()

    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []), default=str)
    }

def buscar_por_id(event, table):
    passenger_id = int(event["pathParameters"]["id"])

    response = table.get_item(
        Key={"PassengerId": passenger_id}
    )

    item = response.get("Item")

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Unknown PassengerId"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(item, default=str)
    }

def deletar(event, table):
    passenger_id = int(event["pathParameters"]["id"])

    table.delete_item(
        Key={"PassengerId": passenger_id}
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Deletado com sucesso"})
    }

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
