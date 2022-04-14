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
    if vector is None:
        raise BadDataException()

    # Load pickled model from file and unpickle, if it isn't already loaded

    if model is None:
        with open("video1.pkl", 'rb') as f:
            model = pickle.load(f)

    predictions = model.predict([vector])
    print("predictions:", predictions)
    prediction = predictions[0]
    return prediction

def lambda_handler(event, context):
    return standardHandler(event, context, main)
