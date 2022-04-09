import json
import pickle
# import sklearn
from library import *

model = None


def main(event):
    global model

    video = json.loads(event['body'])
    print("video", video)
    vector = regularlizeVideo(video)
    print("vector", vector)

    # Load pickled model from file and unpickle, if it isn't already loaded

    if model is None:
        with open("video1.pkl", 'rb') as f:
            model = pickle.load(f)

    predictions = model.predict([vector])
    print("predictions:", predictions)
    prediction = predictions[0]
    return prediction

def lambda_handler(event, context):

    print(f"the event is {event}")
    try:
        prediction = main(event)
        return {
            'statusCode': 200,
            'body': json.dumps({"bestGuess": prediction}),
            'headers': {
                "Access-Control-Allow-Origin" : "*",
            }
        }
    except BaseException as err:
        print({
            'statusCode': 500,
            'body': '"' + str(err) + '"',
            'headers': {
                "Access-Control-Allow-Origin" : "*",
            }
        })
        return {
            'statusCode': 500,
            'body': '"' + str(err) + '"',
            'headers': {
                "Access-Control-Allow-Origin" : "*",
            }
        }

