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

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "pipeline_model.pkl")

with open(MODEL_PATH, "rb") as f:
    pipe = pickle.load(f)


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        data = body.get("data")

        if not data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Json inválido - campo 'data' ausente"})
            }

        prediction = pipe.predict(data)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "prediction": prediction
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }