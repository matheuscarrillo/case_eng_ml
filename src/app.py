# import pickle
# import json

# pipe = pickle.load(open('src/model/pipeline_model.pkl', 'rb'))
# json_data = json.loads("""{"data": [
#             {
#                 "PassengerId": 771,
#                 "Pclass": 3,
#                 "Name": "Lievens, Mr. Rene Aime",
#                 "Sex": "male",
#                 "Age": 24.0,
#                 "SibSp": 0,
#                 "Parch": 0,
#                 "Ticket": "345781",
#                 "Fare": 9.5,
#                 "Cabin": null,
#                 "Embarked": "S"
#             }
#         ]}""")

# json_data = json_data.get("data")


# print(pipe.predict(json_data))

import json
import pickle
import os
import boto3
from utils.transformer import JsonToDF, FeatureEngineering, Model, buscar_por_id, listar_sobreviventes, criar_sobrevivente, deletar
import logging

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "pipeline_model.pkl")

with open(MODEL_PATH, "rb") as f:
    pipe = pickle.load(f)

dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")
table = dynamodb.Table("sobreviventes")


def lambda_handler(event, context):

    method = event.get("httpMethod")
    path = event.get("path")
    logger.info(f"Recebendo requisição: {method} {path}")

    if method == "POST" and path == "/sobreviventes":
        logger.info("Scorando a probabilidade de sobrevivência e criando um novo sobrevivente")
        return criar_sobrevivente(event, pipe=pipe, table=table)

    elif method == "GET" and path == "/sobreviventes":
        logger.info("Listando sobreviventes")
        return listar_sobreviventes(table=table)

    elif method == "GET" and path.startswith("/sobreviventes/"):
        logger.info("Buscando sobrevivente por ID")
        return buscar_por_id(event, table=table)

    elif method == "DELETE" and path.startswith("/sobreviventes/"):
        logger.info("Deletando sobrevivente por ID")
        return deletar(event, table=table)

    return {
        "statusCode": 404,
        "body": "Rota não encontrada"
    }