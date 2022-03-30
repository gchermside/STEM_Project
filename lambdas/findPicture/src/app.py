import json
import pickle
import sklearn

model = None

def lambda_handler(event, context):
    global model

    print(f"the event is {event}")
    landmarks = json.loads(event['body'])
    print("landmarks", landmarks)

    # Load pickled model from file and unpickle, if it isn't already loaded
    if model is None:
        with open("picture.pkl", 'rb') as f:
            model = pickle.load(f)

    predictions = model.predict([landmarks])
    print("predictions:", predictions)
    prediction = predictions[0]


    return {
        'statusCode': 200,
        'body': json.dumps({"bestGuess": prediction}),
        'headers': {
            "Access-Control-Allow-Origin" : "*",
        }
    }
