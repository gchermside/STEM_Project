import json
import pickle
import sklearn

model = None

def lambda_handler(event, context):
    global model

    print(f"the event is {event}")
    landmarks = event['body']
    print(landmarks)

    # Load pickled model from file and unpickle, if it isn't already loaded
    if model is None:
        with open("picture.pkl", 'rb') as f:
            model = pickle.load(f)


    return {
        'statusCode': 200,
        'body': json.dumps({"bestGuess": "g"}),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
        }
    }
