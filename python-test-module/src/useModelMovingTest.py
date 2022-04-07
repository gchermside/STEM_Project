# C:\Users\Genevieve\Documents\programming\STEM_Project\uploads\2022-03-27T02_15_21.496Z-5392117
# C:/Users/Genevieve/Documents/programming/STEM_Project/s3Data/uploads/2022-03-27T02_15_21.496Z-5392117/landmarks.json
import json
import pickle
import sklearn

model = None



def interpolateCoordinate(p1, p2, percent):
    return ((p2-p1) * percent) + p1


def interpolatePoint(p1, p2, percent):
    newPoint = {'x': interpolateCoordinate(p1['x'], p2['x'], percent),
                'y': interpolateCoordinate(p1['y'], p2['y'], percent),
                'z': interpolateCoordinate(p1['z'], p2['z'], percent)}
    return newPoint


def interpolateHand(hand1, hand2, percent):
    newHand = []
    assert len(hand1) == len(hand2)
    for i in range(0, len(hand1)):
        newPoint = interpolatePoint(hand1[i], hand2[i], percent)
        newHand.append(newPoint)
    for point in newHand:
        p = point['x']
        if p<-20 or p>100:
            print(f"point is {p}")
    return newHand

def doHand(NUM_OF_FRAMES, video, hand1or2, newVideoStart):
    newVideo = newVideoStart
    newVideoSpot = 0
    fractions = []
    indexes = []
    for index in range(0, len(video)):
        if len(video[index]) -1 >= hand1or2:
            indexes.append(index)
    length = indexes[-1] - indexes[0] + 1
    for index in indexes:
        fractions.append((index-indexes[0])/(length-1))
    assert fractions[0] == 0 and fractions[-1] == 1
    print("indexes ", indexes)
    print("fractions is ", fractions)
    for num in range(0, NUM_OF_FRAMES):
        d = num/(NUM_OF_FRAMES-1)
        print("d is ",d)
        assert 0 <= d <= 1
        for frameNum in range(0, len(fractions)):
            if d == fractions[frameNum]:
                newHand = video[indexes[frameNum]][hand1or2]
                print("newHand is ", newHand)
                newVideo[newVideoSpot].append(newHand)
                print("newVideoSpot", newVideoSpot)
                newVideoSpot += 1
                break
            elif d < fractions[frameNum]:
                assert frameNum > 0
                hand1 = video[indexes[frameNum-1]][hand1or2]
                hand2 = video[indexes[frameNum]][hand1or2]
                percent = (d-fractions[frameNum-1])/(fractions[frameNum] - fractions[frameNum-1])
                newHand = interpolateHand(hand1, hand2, percent)
                newVideo[newVideoSpot].append(newHand)
                print("newVideoSpot", newVideoSpot)
                newVideoSpot += 1
                break
        else:
            assert False
    assert len(newVideo) == NUM_OF_FRAMES
    return newVideo



def regularlizeVideo(video):
    NUM_OF_FRAMES = 15
    newVideo = []
    for num in range(0, NUM_OF_FRAMES):
        newVideo.append([])
    print("new video is ", newVideo)
    FRACTION_FOR_VIDEO_HANDEDNESS = 0.75
    frames1 = 0
    frames2 = 0
    if len(video) < 5:
        return None
    for frame in video:
        if len(frame) == 0:
            print("empty frame")
        elif len(frame) == 1:
            frames1 += 1
        else:
            print("two hands")
            frames2 += 1
    if frames1/len(video) > FRACTION_FOR_VIDEO_HANDEDNESS:
        #This is a one handed sign
        newVideo = doHand(NUM_OF_FRAMES, video, 0, newVideo)
        return regularizeAndVectorVideo(newVideo)

    elif frames2 >= frames1:
        # this is a two handed sign
        newVideo = doHand(NUM_OF_FRAMES, video, 0, newVideo)
        print("first new video ", newVideo)
        newVideo = doHand(NUM_OF_FRAMES, video, 1, newVideo)
        print("finished video is ", newVideo)
        return regularizeAndVectorVideo(newVideo)
    else:
        print("this sign is ambiguous, will use later")
        return None

def regularizeAndVectorVideo(video):
    videoVector = []
    for frame in video:
        for hand in frame:
            handVector = []
            handVector.append(hand[0]["x"])
            handVector.append(hand[0]["y"])
            handVector.append(hand[0]["z"])
            newHand = regularizeJsonHand(hand)
            vector = vectorHand(newHand)
            for num in vector:
                handVector.append(num)
            for thing in handVector:
                videoVector.append(thing)
    return videoVector



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

def vectorHand(hand):
    vector = []
    for point in hand:
        try:
            vector.append(point['x'])
            vector.append(point['y'])
            vector.append(point['z'])
        except:
            print("error in vector")
            print(f"hand is {hand}")
            return None
    print('video vector len is ', len(vector))
    return vector

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


# def lambda_handler(event, context):
#
#     print(f"the event is {event}")
#     try:
#         prediction = main(event)
#         return {
#             'statusCode': 200,
#             'body': json.dumps({"bestGuess": prediction}),
#             'headers': {
#                 "Access-Control-Allow-Origin" : "*",
#             }
#         }
#     except BaseException as err:
#         return {
#             'statusCode': 500,
#             'body': '"' + str(err) + '"',
#             'headers': {
#                 "Access-Control-Allow-Origin" : "*",
#             }
#         }
#
