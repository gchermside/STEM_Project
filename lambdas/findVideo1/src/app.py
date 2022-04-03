import json
import pickle
import sklearn

model = None


def toVectorandRegularize(image):
    vector = []
    if len(image) == 1:
        for unRegHand in image:
            hand = regularizeJsonHand(unRegHand)
            for points in hand:
                vector.append(points["x"])
                vector.append(points["y"])
                vector.append(points["z"])
    return vector

# this function points moves the hand so the wrist is at 0,0 and makes it a consistant
# porportion(the length between point 0 and 1 will always be the same on hands)
def regularizeJsonHand(originalHand):
    hand = originalHand
    xShift = hand[0]["x"]
    yShift = hand[0]["y"]
    zShift = hand[0]["z"]
    for lm in hand:
        lm["x"] = lm["x"] - xShift
        lm["y"] = lm["y"] - yShift
        lm["z"] = lm["z"] - zShift
    p1 = hand[1]
    mult = 1/(((p1["x"])**2 + (p1["y"])**2 + (p1["z"])**2)**(1/2))
    for lm in hand:
        lm["x"] = lm["x"] * mult
        lm["y"] = lm["y"] * mult
        lm["z"] = lm["z"] * mult
    return hand


def main(event):
    global model

    landmarks = json.loads(event['body'])
    print("landmarks", landmarks)
    vector = toVectorandRegularize(landmarks)
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
        return {
            'statusCode': 500,
            'body': '"' + str(err) + '"',
            'headers': {
                "Access-Control-Allow-Origin" : "*",
            }
        }

